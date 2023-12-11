from ete3 import NCBITaxa
import pandas as pd
import sys

blast_output_file = sys.argv[1]
mapping_file = sys.argv[2]

def parse_taxonomic_mapping(mapping_file):
    mapping = {}
    with open(mapping_file, 'r') as f:
        for line in f:
            accession, taxon_id = line.strip().split('\t')
            mapping[accession] = int(taxon_id)
    return mapping

def extract_kpcofgs(lineage, ranks_order, ncbi):
    kpcofgs = []
    for rank in ranks_order:
        taxid = next((tid for tid in lineage if ncbi.get_rank([tid])[tid] == rank and tid), None)
        kpcofgs.append(taxid if taxid else "")
    return [tid for tid in kpcofgs if tid]  # Filter out empty strings

def find_lowest_common_rank(blast_output_file, mapping_file):
    ncbi = NCBITaxa()
    mapping = parse_taxonomic_mapping(mapping_file)
    sample_data = {}

    with open(blast_output_file, 'r') as blast_file:
        for line in blast_file:
            columns = line.strip().split('\t')
            query_id, subject_id = columns[0], columns[1]

            if query_id not in sample_data:
                sample_data[query_id] = []
            sample_data[query_id].append(subject_id)

    ranks_order = ['species', 'genus', 'family', 'order', 'class', 'phylum', 'kingdom']
    ranks_output_order = ['kingdom', 'phylum', 'class', 'order', 'family','genus','species']

    for query_id, subject_ids in sample_data.items():
        lineage_lists = []
        for subject_id in subject_ids:
            if subject_id in mapping:
                try:
                    taxon_id = mapping[subject_id]
                    lineage = ncbi.get_lineage(taxon_id)
                    kpcofgs_lineage = extract_kpcofgs(lineage, ranks_order, ncbi)  # Extract KPCOFGS
                    lineage_lists.append(kpcofgs_lineage)
                except Exception as e:
                    print(f"Error processing Sample {query_id}: {e}")
                    #row_dict = {'Query ID' : query_id,'Lineage.name' : "Unassigned", 'Lowest Common Rank' : "Unassigned", 'Taxon Name' : "Unassigned"}
                    #results_dict.append(row_dict)

        if not lineage_lists:
            print(f"Query ID: {query_id}")
            print("No valid subject IDs found\n")
            row_dict = {'Query ID' : query_id,'Lineage.name' : "Unassigned", 'Lowest Common Rank' : "Unassigned", 'Taxon Name' : "Unassigned"}
            results_dict.append(row_dict)

            continue

        common_ranks = {}
        for rank in ranks_order:
            taxon_ids_with_rank = []
            for lineage in lineage_lists:
                ranks = ncbi.get_rank(lineage)
                taxon_id = next((taxid for taxid in lineage if ranks.get(taxid) == rank), None)
                if taxon_id:
                    taxon_ids_with_rank.append(taxon_id)
            common_ranks[rank] = taxon_ids_with_rank

        lowest_common_rank = None
        for rank, taxon_ids in common_ranks.items():
            if len(set(taxon_ids)) == 1 and taxon_ids[0] != "":
                lowest_common_rank = rank
                break

        if lowest_common_rank:
            taxon_ids = common_ranks[lowest_common_rank]
            common_rank_taxon_id = min(taxon_ids)
            common_rank_taxa = ncbi.get_taxid_translator([common_rank_taxon_id])[common_rank_taxon_id]
            common_rank_lineage = ncbi.get_lineage(common_rank_taxon_id)
            kpcofgs_lineage = extract_kpcofgs(common_rank_lineage, ranks_output_order, ncbi)
            kpcofgs_names = ncbi.get_taxid_translator(kpcofgs_lineage)
            kpcofgs_names_list = [kpcofgs_names[taxid] for taxid in kpcofgs_lineage]

            print(f"Query ID: {query_id}")
            print(f"Lowest Common Rank: {lowest_common_rank}: {common_rank_taxa}")
            row_dict = {'Query ID' : query_id,'Lineage.name' : kpcofgs_names_list, 'Lowest Common Rank' : lowest_common_rank, 'Taxon Name' : common_rank_taxa}
            results_dict.append(row_dict)


result_df = pd.DataFrame(columns=['Query ID', 'Lineage.name', 'Lowest Common Rank', 'Taxon Name'])
results_dict = []
find_lowest_common_rank(blast_output_file, mapping_file)
result_df =pd.DataFrame.from_dict(results_dict)
result_df.to_csv("LCA.out", index=False)

print("")
print("Please Check LCA.out")
