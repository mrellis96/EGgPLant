#!/usr/bin/python3
# EGgPLant Lowest Common Ancestor Script - V1.2
import os
import sys
import time
import pandas as pd
from ete3 import NCBITaxa


def initialize_ncbi(max_age_days=7):
    """Initializes NCBITaxa and updates the database only if it is missing

    or older than the specified max_age_days.
    """
    print("Checking NCBI taxonomy database status...")

    # Default ete3 database location
    db_path = os.path.expanduser("~/.etetoolkit/taxa.sqlite")
    needs_update = False

    if not os.path.exists(db_path):
        print("Database not found. Initiating fresh download...")
        needs_update = True
    else:
        file_mod_time = os.path.getmtime(db_path)
        current_time = time.time()
        age_in_days = (current_time - file_mod_time) / (24 * 3600)

        if age_in_days > max_age_days:
            print(
                f"Database is {age_in_days:.1f} days old. Initiating update..."
            )
            needs_update = True
        else:
            print(f"Database is {age_in_days:.1f} days old. Skipping update.")
            

    ncbi = NCBITaxa()
    if needs_update:
        ncbi.update_taxonomy_database()

    return ncbi

ncbi = initialize_ncbi(max_age_days=7)

# Fixed ranks setup
RANKS_ORDER = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']

def parse_taxonomic_mapping(mapping_file):
    """Parses accession-to-taxid mapping file efficiently."""
    mapping = {}
    with open(mapping_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                mapping[parts[0]] = int(parts[1])
    return mapping

def clean_column(column):
    """Trims trailing symbols from BLAST output fields."""
    if '###' in column:
        return column.split('###')[0]
    if ';' in column:
        return column.split(';')[0]
    return column

def parse_blast_output(blast_output_file):
    """Reads BLAST file and aggregates candidate hits per query."""
    sample_data = {}
    with open(blast_output_file, 'r') as f:
        for line in f:
            columns = line.strip().split('\t')
            if len(columns) < 4:
                continue
            
            query_id = clean_column(columns[0])
            subject_id = clean_column(columns[1])
            perc_id = float(clean_column(columns[2]))
            qcov = float(clean_column(columns[3]))

            # Broadest filter: capture all hits >= 90% identity and > 95% coverage
            if perc_id >= 90.0 and qcov > 95.0:
                sample_data.setdefault(query_id, []).append((subject_id, perc_id))
    return sample_data

def get_cascading_subjects(hits):
    """Applies the user's cascading percentage identity filters."""
    for threshold in [100.0, 98.0, 95.0, 90.0]:
        subjects = [sub for sub, pid in hits if pid >= threshold]
        if subjects:
            return subjects
    return []

def find_lowest_common_ancestor(lineages, ncbi):
    """
    Finds the lowest common taxid from a list of lineages.
    Lineages are lists of taxids ordered from root (Kingdom) to leaf (Species).
    """
    if not lineages:
        return None
    
    # Intersect step-by-step from the root downward
    common_lineage = []
    for level_tids in zip(*lineages):
        if len(set(level_tids)) == 1:  # All lineages agree at this depth
            common_lineage.append(level_tids[0])
        else:
            break  # Disagreement found; stop here
            
    return common_lineage[-1] if common_lineage else None

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <blast_output> <mapping_file>")
        sys.exit(1)

    blast_output_file = sys.argv[1]
    mapping_file = sys.argv[2]

    mapping = parse_taxonomic_mapping(mapping_file)
    sample_data = parse_blast_output(blast_output_file)
    
    results = []

    print("Processing queries and resolving lineages...")
    for query_id, hits in sample_data.items():
        subject_ids = get_cascading_subjects(hits)

        if not subject_ids:
            print(f"Error processing Sample {query_id}: no matches found within thresholds")
            results.append({'Query ID': query_id, 'Lineage.name': "Unassigned", 'Lowest Common Rank': "Unassigned", 'Taxon Name': "Unassigned"})
            continue

        # Collect unique target taxids for this specific query
        valid_taxids = set()
        for sub in subject_ids:
            if sub in mapping:
                valid_taxids.add(mapping[sub])

        if not valid_taxids:
            print(f"Query ID: {query_id}: No valid subject IDs found in taxonomy map.")
            results.append({'Query ID': query_id, 'Lineage.name': "Unassigned", 'Lowest Common Rank': "Unassigned", 'Taxon Name': "Unassigned"})
            continue

        # 1. Fetch full lineages for all matching taxids
        # Bulk query get_lineage to minimize DB hits
        raw_lineages = [ncbi.get_lineage(tid) for tid in valid_taxids]
        
        # 2. Gather all unique taxids present in these paths to translate ranks/names in bulk
        all_path_tids = set(tid for lin in raw_lineages for tid in lin)
        rank_map = ncbi.get_rank(all_path_tids)
        
        # 3. Filter lineages down to just the standard KPCOFGS ranks, ordered root-to-leaf
        standard_lineages = []
        for lin in raw_lineages:
            # Build an ordered root-to-leaf list corresponding to RANKS_ORDER
            filtered_lin = []
            for rank in RANKS_ORDER:
                match = [t for t in lin if rank_map.get(t) == rank]
                if match:
                    filtered_lin.append(match[0])
            if filtered_lin:
                standard_lineages.append(filtered_lin)

        # 4. Find the LCA TaxID using zip aggregation
        lca_taxid = find_lowest_common_ancestor(standard_lineages, ncbi)

        if lca_taxid:
            lca_rank = rank_map.get(lca_taxid, "unknown")
            
            # Fetch the complete standardized lineage path for the resolved LCA node
            lca_full_lineage = ncbi.get_lineage(lca_taxid)
            ordered_lca_tids = []
            for rank in RANKS_ORDER:
                match = [t for t in lca_full_lineage if rank_map.get(t) == rank]
                if match:
                    ordered_lca_tids.append(match[0])

            # Bulk translate names for output row
            name_map = ncbi.get_taxid_translator(ordered_lca_tids + [lca_taxid])
            
            kpcofgs_names_list = [name_map.get(tid, "") for tid in ordered_lca_tids]
            taxon_name = name_map.get(lca_taxid, "Unknown")

            print(f"Query ID: {query_id} -> LCA: {lca_rank}: {taxon_name}")
            
            results.append({
                'Query ID': query_id, 
                'Lineage.name': kpcofgs_names_list, 
                'Lowest Common Rank': lca_rank, 
                'Taxon Name': taxon_name
            })
        else:
            results.append({'Query ID': query_id, 'Lineage.name': "Unassigned", 'Lowest Common Rank': "Unassigned", 'Taxon Name': "Unassigned"})

    # Save outputs efficiently with Pandas
    result_df = pd.DataFrame.from_dict(results)
    result_df.to_csv("LCA.csv", index=False, sep=',')
    print("\nProcessing complete. Please check LCA.csv")

if __name__ == "__main__":
    main()