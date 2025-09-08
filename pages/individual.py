import streamlit as st
from backend import process_locid, process_mlocid, df, show_protein_ppi_data, mlocid_error
from pages.mainapp import base_footer

def ppi_info_page():
    st.title("Protein Protein Interaction")
    st.write("**It gives the details about the interacting partners of a protein and interactions effects the functions of a genes**")
    col1, col2 = st.columns(2)

    with col1:
        con1 = st.container(border=True)
        tid = con1.text_input("Enter the Gene ID: ", placeholder="e.g., Ca_00001", key="ppi_Tid_input1").strip()
        mtid = con1.text_input("Enter multiple Gene IDs: ", placeholder="e.g., Ca_00001, Ca_00002", key="ppi_mTid_input2").strip()
        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)

    with col2:
        con2 = st.container(border=True)
        locid = con2.text_input("Enter the NCBI ID: ", placeholder="e.g., LOC101511858", key="ppi_Locid_input1").strip()
        mlocid = con2.text_input("Enter multiple NCBI IDs: ", placeholder="e.g., LOC101511858, LOC101496413", key="ppi_mLocid_input2").strip()
        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)

    cc1, cc2, cc3 = st.columns([2, 2, 2])
    with cc2:
        start_button = st.button("Search", use_container_width=True, key="ppi_Searchbutton1")

    if start_button:
        if tid:
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]

                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Protein Protein Interaction")
                        show_protein_ppi_data(tid)
                else:
                    st.error(f"No match found for Gene ID: {tid}")

            st.toast("Task completed successfully.")
            
        elif mtid:
            mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
            mtid_list.sort()
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_rows = df[df['Transcript id'].isin(mtid_list)]
                found_ids = matching_rows['Transcript id'].unique().tolist()
                not_found_ids = [x for x in mtid_list if x not in found_ids]

                if not matching_rows.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Protein Protein Interaction")
                        show_protein_ppi_data(mtid_list, is_multi=True)

                if not_found_ids:
                    st.error(f"No matches found for Gene IDs: {', '.join(not_found_ids)}")
            st.toast("Task completed successfully.")
            
        elif locid:
            tid = process_locid(locid)
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]

                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Protein Protein Interaction")
                        show_protein_ppi_data(tid)
                else:
                    st.error(f"No match found for NCBI ID: {locid}")
            
            st.toast("Task completed successfully.")
            
        elif mlocid:
            available, rejected = mlocid_error(mlocid)
            if available:
                mtid = process_mlocid(",".join(available))
                mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
                mtid_list.sort()
                if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                    matching_rows = df[df['Transcript id'].isin(mtid_list)]
                    if not matching_rows.empty:
                        con = st.container(border=True)
                        with con:
                            st.subheader("Protein Protein Interaction")
                            show_protein_ppi_data(mtid_list, is_multi=True)
                st.toast("Task completed successfully.")

            if rejected:
                st.error(f"No matches found for NCBI IDs: {', '.join(rejected)}")
            
        else:
            st.warning("Need either a Gene ID or NCBI ID to proceed.")
            
    elif tid == "":
        st.warning("Need Gene ID to proceed.")
    else:
        st.write("Press the 'Search' button to begin ...")
        st.write("Follow the instructions or check out tutorials")

    base_footer()
    return


from backend import process_locid, process_mlocid, df, show_mirna_data, mlocid_error


def mirna_info_page():
    st.title("miRNA Target")
    st.write("**Users can get the details about the putative miRNAs of the particular gene**")
    col1, col2 = st.columns(2)
    with col1:
        c1 = st.container(border=True)
        tid = c1.text_input("Enter the Gene ID: ", placeholder="e.g., Ca_00001", key="mirna_Tid_input1").strip(); mtid = c1.text_input("Enter multiple Gene IDs: ", placeholder="e.g., Ca_00001, Ca_00002", key="mirna_mTid_input2").strip()
        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)
    with col2:
        c2 = st.container(border=True)
        locid = c2.text_input("Enter the NCBI ID: ", placeholder="e.g., LOC101511858", key="mirna_Locid_input1").strip()
        mlocid = c2.text_input("Enter multiple NCBI IDs: ", placeholder="e.g., LOC101511858, LOC101496413", key="mirna_mLocid_input2").strip()
        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)
    cc1, cc2, cc3 = st.columns([2, 2, 2])
    with cc2:
        start_button = st.button("Search", use_container_width=True, key="mirna_Searchbutton1")

    if start_button:
        if tid:
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("miRNA Target")
                        show_mirna_data(tid)
                else:
                    st.error(f"No match found for Gene ID: {tid}")
            st.toast("Task completed successfully.")
        elif mtid:
            mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
            mtid_list.sort()
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_rows = df[df['Transcript id'].isin(mtid_list)]
                found_ids = matching_rows['Transcript id'].unique().tolist()
                not_found_ids = [x for x in mtid_list if x not in found_ids]
                if not matching_rows.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("miRNA Target")
                        show_mirna_data(mtid_list, is_multi=True)
                if not_found_ids:
                    st.error(f"No matches found for Gene IDs: {', '.join(not_found_ids)}")
            st.toast("Task completed successfully.")
        elif locid:
            tid = process_locid(locid)
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("miRNA Target")
                        show_mirna_data(tid)
                else:
                    st.error(f"No match found for NCBI ID: {locid}")
            st.toast("Task completed successfully.")
        elif mlocid:
            available, rejected = mlocid_error(mlocid)
            if available:
                mtid = process_mlocid(",".join(available))
                mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
                mtid_list.sort()
                if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                    matching_rows = df[df['Transcript id'].isin(mtid_list)]
                    if not matching_rows.empty:
                        con = st.container(border=True)
                        with con:
                            st.subheader("miRNA Target")
                            show_mirna_data(mtid_list, is_multi=True)
                st.toast("Task completed successfully.")
            if rejected:
                st.error(f"No matches found for NCBI IDs: {', '.join(rejected)}")
        
        else:
            st.warning("Need either a Gene ID or NCBI ID to proceed.")
    elif tid == "":
        st.warning("Need Gene ID to proceed.")
    else:
        st.write("Press the 'Search' button to begin ...")
        st.write("Follow the instructions or check out tutorials")

    base_footer()
    return

from backend import process_locid, process_mlocid, df, show_rna_data, show_lncrna_data, mlocid_error

def rna_type_page():
    st.title("RNA type Search")
    st.write("**It gives details about the coding potential of RNA (mRNA or LncRNA)**")
    col1, col2 = st.columns(2)

    with col1:
        con1 = st.container(border=True)
        tid = con1.text_input("Enter the Gene ID: ", placeholder="e.g., Ca_00001", key="rna_Tid_input1").strip()
        mtid = con1.text_input("Enter multiple Gene IDs: ", placeholder="e.g., Ca_00001, Ca_00002", key="rna_mTid_input2").strip()
        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)

    with col2:
        con2 = st.container(border=True)
        locid = con2.text_input("Enter the NCBI ID: ", placeholder="e.g., LOC101511858", key="rna_Locid_input1").strip()
        mlocid = con2.text_input("Enter multiple NCBI IDs: ", placeholder="e.g., LOC101511858, LOC101496413", key="rna_mLocid_input2").strip()
        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)

    con_btn1, con_btn2, con_btn3 = st.columns([2, 2, 2])
    with con_btn2:
        start_button = st.button("Search", use_container_width=True, key="rna_Searchbutton1")

    if start_button:
        if tid:
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]

                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("RNA")
                        show_rna_data(tid)

                        st.subheader("lncRNA")
                        show_lncrna_data(tid)
                else:
                    st.error(f"No match found for Gene ID: {tid}")
            st.toast("Task completed successfully.")

        elif mtid:
            mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
            mtid_list.sort()
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_rows = df[df['Transcript id'].isin(mtid_list)]
                found_ids = matching_rows['Transcript id'].unique().tolist()
                not_found_ids = [x for x in mtid_list if x not in found_ids]
                if not matching_rows.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("RNA")
                        show_rna_data(mtid_list, is_multi=True)

                        st.subheader("lncRNA")
                        show_lncrna_data(mtid_list, is_multi=True)
                if not_found_ids:
                    st.error(f"No matches found for Gene IDs: {', '.join(not_found_ids)}")

            st.toast("Task completed successfully.")

        elif locid:
            tid = process_locid(locid)
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]

                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("RNA")
                        show_rna_data(tid)

                        st.subheader("lncRNA")
                        show_lncrna_data(tid)
                else:
                    st.error(f"No match found for NCBI ID: {locid}")

            st.toast("Task completed successfully.")

        elif mlocid:
            available, rejected = mlocid_error(mlocid)
            if available:
                mtid = process_mlocid(",".join(available))
                mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
                mtid_list.sort()
                if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                    matching_rows = df[df['Transcript id'].isin(mtid_list)]
                    if not matching_rows.empty:
                        con = st.container(border=True)
                        with con:
                            st.subheader("RNA")
                            show_rna_data(mtid_list, is_multi=True)

                            st.subheader("lncRNA")
                            show_lncrna_data(mtid_list, is_multi=True)
                st.toast("Task completed successfully.")

            if rejected:
                st.error(f"No matches found for NCBI IDs: {', '.join(rejected)}")

        else:
            st.warning("Need either a Gene ID or NCBI ID to proceed.")
    elif tid == "":
        st.warning("Need Gene ID to proceed.")
    else:
        st.write("Press the 'Search' button to begin ...")
        st.write("Follow the instructions or check out tutorials")

    base_footer()
    return

from backend import process_locid, process_mlocid, df, show_snp_data, mlocid_error

def snp_info_page():
    st.title("Single Nucleotide Polymorphism Calling")
    st.write("**It gives the details of putative SNP variations obtained from the chickpea pangenome**")
    col1, col2 = st.columns(2)

    with col1:
        con1 = st.container(border=True)
        tid = con1.text_input("Enter the Gene ID: ", placeholder="e.g., Ca_00001", key="snp_Tid_input1").strip(); mtid = con1.text_input("Enter multiple Gene IDs: ", placeholder="e.g., Ca_00001, Ca_00002", key="snp_mTid_input2").strip()
        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)

    with col2:
        con2 = st.container(border=True)
        locid = con2.text_input("Enter the NCBI ID: ", placeholder="e.g., LOC101511858", key="snp_Locid_input1").strip()
        mlocid = con2.text_input("Enter multiple NCBI IDs: ", placeholder="e.g., LOC101511858, LOC101496413", key="snp_mLocid_input2").strip()
        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)

    c1, c2, c3 = st.columns([2, 2, 2])
    with c2:
        start_button = st.button("Search", use_container_width=True, key="snp_Searchbutton1")

    if start_button:
        if tid:
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Single Nucleotide Polymorphism (SNP)")
                        show_snp_data(tid)
                else:
                    st.error(f"No match found for Gene ID: {tid}")
            st.toast("Task completed successfully.")
        elif mtid:
            mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
            mtid_list.sort()
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_rows = df[df['Transcript id'].isin(mtid_list)]
                found_ids = matching_rows['Transcript id'].unique().tolist()
                not_found_ids = [x for x in mtid_list if x not in found_ids]
                if not matching_rows.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Single Nucleotide Polymorphism (SNP)")
                        show_snp_data(mtid_list, is_multi=True)
                if not_found_ids:
                    st.error(f"No matches found for Gene IDs: {', '.join(not_found_ids)}")
            st.toast("Task completed successfully.")
        elif locid:
            tid = process_locid(locid)
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Single Nucleotide Polymorphism (SNP)")
                        show_snp_data(tid)
                else:
                    st.error(f"No match found for NCBI ID: {locid}")
            st.toast("Task completed successfully.")
        elif mlocid:
            available, rejected = mlocid_error(mlocid)
            if available:
                mtid = process_mlocid(",".join(available))
                mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
                mtid_list.sort()
                if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                    matching_rows = df[df['Transcript id'].isin(mtid_list)]
                    if not matching_rows.empty:
                        con = st.container(border=True)
                        with con:
                            st.subheader("Single Nucleotide Polymorphism (SNP)")
                            show_snp_data(mtid_list, is_multi=True)
                st.toast("Task completed successfully.")

            if rejected:
                st.error(f"No matches found for NCBI IDs: {', '.join(rejected)}")
        
        else:
            st.warning("Need either a Gene ID or NCBI ID to proceed.")
    elif tid == "":
        st.warning("Need Gene ID to proceed.")
    else:
        st.write("Press the 'Search' button to begin ...")
        st.write("Follow the instructions or check out tutorials")

    base_footer()
    return

from backend import process_locid, process_mlocid, df, show_fpkm_matrix, mlocid_error

def spatial_info_page():

    st.title("Spatial Expression Search")
    st.write("**It provides the information about the temporal expression among 32 different developmental stages**")

    col1, col2 = st.columns(2)

    with col1:
        con1 = st.container(border=True)
        tid = con1.text_input("Enter the Gene ID: ",placeholder="e.g., Ca_00001",key="spatial_Tid_input1").strip()

        mtid = con1.text_input("Enter multiple Gene IDs: ",placeholder="e.g., Ca_00001, Ca_00002",key="spatial_mTid_input2").strip()

        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)

    with col2:
        con2 = st.container(border=True)
        locid = con2.text_input("Enter the NCBI ID: ",placeholder="e.g., LOC101511858",key="spatial_Locid_input1").strip()

        mlocid = con2.text_input("Enter multiple NCBI IDs: ",placeholder="e.g., LOC101511858, LOC101496413",key="spatial_mLocid_input2").strip()

        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)

    con_btn1, con_btn2, con_btn3 = st.columns([2, 2, 2])
    with con_btn2:
        start_button = st.button("Search", use_container_width=True, key="spatial_Searchbutton1")

    if start_button:

        # Single Gene ID (tid)
        if tid:
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]

                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Fragments per kilobase of Exon per million mapped fragments Matrix Atlas")
                        show_fpkm_matrix(tid)
                else:
                    st.error(f"No match found for Gene ID: {tid}")

            st.toast("Task completed successfully.")

        # Multiple Gene IDs (mtid)
        elif mtid:
            mtid_list = [gene_id.strip() for gene_id in mtid.replace(",", " ").split()]
            mtid_list.sort()

            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_rows = df[df['Transcript id'].isin(mtid_list)]
                found_ids = matching_rows['Transcript id'].unique().tolist()
                not_found_ids = [x for x in mtid_list if x not in found_ids]

                if not matching_rows.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Fragments per kilobase of Exon per million mapped fragments Matrix Atlas")
                        show_fpkm_matrix(mtid_list, is_multi=True)
                if not_found_ids:
                    st.error(f"No matches found for Gene IDs: {', '.join(not_found_ids)}")

            st.toast("Task completed successfully.")

        # Single NCBI ID (locid)
        elif locid:
            tid = process_locid(locid)
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Fragments per kilobase of Exon per million mapped fragments Matrix Atlas")
                        show_fpkm_matrix(tid)
                else:
                    st.error(f"No match found for NCBI ID: {locid}")
            st.toast("Task completed successfully.")

        # Multiple NCBI IDs (mlocid)
        elif mlocid:
            available, rejected = mlocid_error(mlocid)
            if available:
                mtid = process_mlocid(",".join(available))
                mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
                mtid_list.sort()
                if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                    matching_rows = df[df['Transcript id'].isin(mtid_list)]
                    if not matching_rows.empty:
                        con = st.container(border=True)
                        with con:
                            st.subheader("Fragments per kilobase of Exon per million mapped fragments Matrix Atlas")
                            show_fpkm_matrix(mtid_list, is_multi=True)
                st.toast("Task completed successfully.")

            if rejected:
                st.error(f"No matches found for NCBI IDs: {', '.join(rejected)}")

        else:
            st.warning("Need either a Gene ID or NCBI ID to proceed.")

    elif tid == "":
        st.warning("Need Gene ID to proceed.")
    else:
        st.write("Press the 'Search' button to begin ...")
        st.write("Follow the instructions or check out tutorials")

    base_footer()
    return

from backend import process_locid, process_mlocid, df, show_orthologs_data, show_inparalogs_data, mlocid_error

def orthologs_info_page():
    st.title("Orthologs/Paralogs")
    st.write("**Users can get the details about the conserveness in gene sequences among/within genome of various crop plants**")
    col1, col2 = st.columns(2)
    with col1:
        c1 = st.container(border=True)
        tid = c1.text_input("Enter the Gene ID: ", placeholder="e.g., Ca_00001", key="orth_Tid_input1").strip(); mtid = c1.text_input("Enter multiple Gene IDs: ", placeholder="e.g., Ca_00001, Ca_00002", key="orth_mTid_input2").strip()
        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)
    with col2:
        c2 = st.container(border=True)
        locid = c2.text_input("Enter the NCBI ID: ", placeholder="e.g., LOC101511858", key="orth_Locid_input1").strip()
        mlocid = c2.text_input("Enter multiple NCBI IDs: ", placeholder="e.g., LOC101511858, LOC101496413", key="orth_mLocid_input2").strip()
        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)
    cc1, cc2, cc3 = st.columns([2, 2, 2])
    with cc2:
        start_button = st.button("Search", use_container_width=True, key="orth_Searchbutton1")

    if start_button:
        if tid:
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Ortholog")
                        show_orthologs_data(tid)
                        st.subheader("Paralog")
                        show_inparalogs_data(tid)
                else:
                    st.error(f"No match found for Gene ID: {tid}")
            st.toast("Task completed successfully.")

        elif mtid:
            mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
            mtid_list.sort()
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_rows = df[df['Transcript id'].isin(mtid_list)]
                found_ids = matching_rows['Transcript id'].unique().tolist()
                not_found_ids = [x for x in mtid_list if x not in found_ids]

                if not matching_rows.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Ortholog")
                        show_orthologs_data(mtid_list, is_multi=True)
                        st.subheader("Paralog")
                        show_inparalogs_data(mtid_list, is_multi=True)
                if not_found_ids:
                    st.error(f"No matches found for Gene IDs: {', '.join(not_found_ids)}")

            st.toast("Task completed successfully.")

        elif locid:
            tid = process_locid(locid)
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Ortholog")
                        show_orthologs_data(tid)
                        st.subheader("Paralog")
                        show_inparalogs_data(tid)
                else:
                    st.error(f"No match found for NCBI ID: {locid}")
            st.toast("Task completed successfully.")

        elif mlocid:
            available, rejected = mlocid_error(mlocid)
            if available:
                mtid = process_mlocid(",".join(available))
                mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
                mtid_list.sort()
                if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                    matching_rows = df[df['Transcript id'].isin(mtid_list)]
                    if not matching_rows.empty:
                        con = st.container(border=True)
                        with con:
                            st.subheader("Ortholog")
                            show_orthologs_data(mtid_list, is_multi=True)
                            st.subheader("Paralog")
                            show_inparalogs_data(mtid_list, is_multi=True)
                st.toast("Task completed successfully.")

            if rejected:
                st.error(f"No matches found for NCBI IDs: {', '.join(rejected)}")

        else:
            st.warning("Need either a Gene ID or NCBI ID to proceed.")

    elif tid == "":
        st.warning("Need Gene ID to proceed.")
    else:
        st.write("Press the 'Search' button to begin ...")
        st.write("Follow the instructions or check out tutorials")

    base_footer()
    return

from backend import process_locid, process_mlocid, df, show_go_kegg_data, mlocid_error

def go_info_page():
    st.title("Gene Ontology and Kyoto Encyclopedia of Genes and Genomes Analysis")
    st.write("**It gives details about the gene functions and their involvement in various molecular pathways**")
    col1, col2 = st.columns(2)
    with col1:
        c1 = st.container(border=True)
        tid = c1.text_input("Enter the Gene ID: ", placeholder="e.g., Ca_00001", key="gokegg_Tid_input1").strip(); mtid = c1.text_input("Enter multiple Gene IDs: ", placeholder="e.g., Ca_00001, Ca_00002", key="gokegg_mTid_input2").strip()
        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)
    with col2:
        c2 = st.container(border=True)
        locid = c2.text_input("Enter the NCBI ID: ", placeholder="e.g., LOC101511858", key="gokegg_Locid_input1").strip()
        mlocid = c2.text_input("Enter multiple NCBI IDs: ", placeholder="e.g., LOC101511858, LOC101496413", key="gokegg_mLocid_input2").strip()
        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)
    cc1, cc2, cc3 = st.columns([2, 2, 2])
    with cc2:
        start_button = st.button("Search", use_container_width=True, key="gokegg_Searchbutton1")

    if start_button:
        if tid:
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Gene Ontology and Kyoto Encyclopedia of Genes and Genomes")
                        show_go_kegg_data(tid)
                else:
                    st.error(f"No match found for Gene ID: {tid}")
            st.toast("Task completed successfully.")
        elif mtid:
            mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
            mtid_list.sort()
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_rows = df[df['Transcript id'].isin(mtid_list)]
                found_ids = matching_rows['Transcript id'].unique().tolist()
                not_found_ids = [x for x in mtid_list if x not in found_ids]
                if not matching_rows.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Gene Ontology and Kyoto Encyclopedia of Genes and Genomes")
                        show_go_kegg_data(mtid_list, is_multi=True)
                if not_found_ids:
                    st.error(f"No matches found for Gene IDs: {', '.join(not_found_ids)}")
            st.toast("Task completed successfully.")
        elif locid:
            tid = process_locid(locid)
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Gene Ontology and Kyoto Encyclopedia of Genes and Genomes")
                        show_go_kegg_data(tid)
                else:
                    st.error(f"No match found for NCBI ID: {locid}")
            st.toast("Task completed successfully.")
        elif mlocid:
            available, rejected = mlocid_error(mlocid)
            if available:
                mtid = process_mlocid(",".join(available))
                mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
                mtid_list.sort()
                if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                    matching_rows = df[df['Transcript id'].isin(mtid_list)]
                    if not matching_rows.empty:
                        con = st.container(border=True)
                        with con:
                            st.subheader("Gene Ontology and Kyoto Encyclopedia of Genes and Genomes")
                            show_go_kegg_data(mtid_list, is_multi=True)
                st.toast("Task completed successfully.")
            if rejected:
                st.error(f"No matches found for NCBI IDs: {', '.join(rejected)}")
        
        else:
            st.warning("Need either a Gene ID or NCBI ID to proceed.")
    elif tid == "":
        st.warning("Need Gene ID to proceed.")
    else:
        st.write("Press the 'Search' button to begin ...")
        st.write("Follow the instructions or check out tutorials")

    base_footer()
    return

from backend import process_locid, process_mlocid, show_sequence_data,df, show_biochemical_properties, mlocid_error

def gene_info_page():
    st.title("Gene Information Search")
    st.write("**It gives detailed insights about each Genomic Sequence, RNA Sequence, CDS Sequence, Promoter Sequences, Peptide Sequence and biochemical properties of each protein.**")
    col1, col2 = st.columns(2)

    with col1:
        con1 = st.container(border=True)
        tid = con1.text_input("Enter the Gene ID: ", placeholder="e.g., Ca_00001", key="ginfo_Tid_input1").strip()
        mtid = con1.text_input("Enter multiple Gene IDs: ", placeholder="e.g., Ca_00001, Ca_00002", key="ginfo_mTid_input2").strip()
        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)

    with col2:
        con2 = st.container(border=True)
        locid = con2.text_input("Enter the NCBI ID: ", placeholder="e.g., LOC101511858", key="ginfo_Locid_input1").strip()
        mlocid = con2.text_input("Enter multiple NCBI IDs: ", placeholder="e.g., LOC101511858, LOC101496413", key="ginfo_mLocid_input2").strip()
        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)

    con1, con2, con3 = st.columns([2, 2, 2])
    with con2:
        start_button = st.button("Search", use_container_width=True, key="ginfo_Searchbutton1")

    if start_button:
        if tid:
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]

                if not matching_row.empty:
                    con=st.container(border=True)
                    with con:
                        st.subheader("Sequence data")
                        show_sequence_data(tid)

                        st.subheader("Biochemical Properties")
                        show_biochemical_properties(tid)
                else:
                    st.error(f"No match found for Gene ID: {tid}")

            st.toast("Task completed successfully.")
            
        elif mtid:
            mtid_list = [tid.strip() for tid in mtid.replace(",", " ").split()]
            mtid_list.sort()

            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_rows = df[df['Transcript id'].isin(mtid_list)]
                found_ids = matching_rows['Transcript id'].unique().tolist()
                not_found_ids = [x for x in mtid_list if x not in found_ids]

                if not matching_rows.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("\nSequences data")
                        show_sequence_data(mtid_list, is_multi=True)

                        st.subheader("Biochemical Properties")
                        show_biochemical_properties(mtid_list, is_multi=True)

                if not_found_ids:
                    st.error(f"No matches found for Gene IDs: {', '.join(not_found_ids)}")

            st.toast("Task completed successfully.")
            
        elif locid:
            tid = process_locid(locid)
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]

                if not matching_row.empty:
                    con=st.container(border=True)
                    with con:
                        st.subheader("Sequence data")
                        show_sequence_data(tid)

                        st.subheader("Biochemical Properties")
                        show_biochemical_properties(tid)
                else:
                    st.error(f"No match found for NCBI ID: {locid}")
            
            st.toast("Task completed successfully.")
            
        elif mlocid:
            available, rejected = mlocid_error(mlocid)
            if available:
                mtid = process_mlocid(",".join(available))
                mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
                mtid_list.sort()
                if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                    matching_rows = df[df['Transcript id'].isin(mtid_list)]
                    if not matching_rows.empty:
                        con = st.container(border=True)
                        with con:
                            st.subheader("\nSequences data")
                            show_sequence_data(mtid_list, is_multi=True)

                            st.subheader("Biochemical Properties")
                            show_biochemical_properties(mtid_list, is_multi=True)
                st.toast("Task completed successfully.")
            if rejected:
                st.error(f"No matches found for NCBI IDs: {', '.join(rejected)}")

            st.toast("Task completed successfully.")
            
    elif tid == "":
        st.warning("Need Gene ID to proceed.")
    else:
        st.write("Press the 'Search' button to begin ...")
        st.write("Follow the instructions or check out tutorials")

    base_footer()
    return

from backend import process_locid, process_mlocid, df, show_cellular_Localization, mlocid_error, show_sequence_data_p

def local_info_page():
    st.title("Localization Search")
    st.write("**It provides the probable cellular location of a gene expression and predicted on the basis of signal sequences**")
    col1, col2 = st.columns(2)
    with col1:
        c1 = st.container(border=True)
        tid = c1.text_input("Enter the Gene ID: ", placeholder="e.g., Ca_00001", key="local_Tid_input1").strip(); mtid = c1.text_input("Enter multiple Gene IDs: ", placeholder="e.g., Ca_00001, Ca_00002", key="local_mTid_input2").strip()
        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)
    with col2:
        c2 = st.container(border=True)
        locid = c2.text_input("Enter the NCBI ID: ", placeholder="e.g., LOC101511858", key="local_Locid_input1").strip()
        mlocid = c2.text_input("Enter multiple NCBI IDs: ", placeholder="e.g., LOC101511858, LOC101496413", key="local_mLocid_input2").strip()
        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)
    cc1, cc2, cc3 = st.columns([2, 2, 2])
    with cc2:
        start_button = st.button("Search", use_container_width=True, key="local_Searchbutton1")

    if start_button:
        if tid:
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Cellular-localization")
                        show_cellular_Localization(tid)
                else:
                    st.error(f"No match found for Gene ID: {tid}")
            st.toast("Task completed successfully.")
        elif mtid:
            mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
            mtid_list.sort()
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_rows = df[df['Transcript id'].isin(mtid_list)]
                found_ids = matching_rows['Transcript id'].unique().tolist()
                not_found_ids = [x for x in mtid_list if x not in found_ids]
                if not matching_rows.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Cellular-localization")
                        show_cellular_Localization(mtid_list, is_multi=True)
                if not_found_ids:
                    st.error(f"No matches found for Gene IDs: {', '.join(not_found_ids)}")
            st.toast("Task completed successfully.")
        elif locid:
            tid = process_locid(locid)
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]
                if not matching_row.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("Cellular-localization")
                        show_cellular_Localization(tid)
                else:
                    st.error(f"No match found for NCBI ID: {locid}")
            st.toast("Task completed successfully.")
        elif mlocid:
            available, rejected = mlocid_error(mlocid)
            if available:
                mtid = process_mlocid(",".join(available))
                mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
                mtid_list.sort()
                if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                    matching_rows = df[df['Transcript id'].isin(mtid_list)]
                    if not matching_rows.empty:
                        con = st.container(border=True)
                        with con:
                            st.subheader("Cellular-localization")
                            show_cellular_Localization(mtid_list, is_multi=True)
                st.toast("Task completed successfully.")

            if rejected:
                st.error(f"No matches found for NCBI IDs: {', '.join(rejected)}")
        else:
            st.warning("Need either a Gene ID or NCBI ID to proceed.")
    elif tid == "":
        st.warning("Need Gene ID to proceed.")
    else:
        st.write("Press the 'Search' button to begin ...")
        st.write("Follow the instructions or check out tutorials")

    base_footer()
    return

def primer_info_page():
    st.title("PRIMER Design and Information")
    st.write("""<p><b>Enter the Gene ID or NCBI ID to fetch the target sequence and then paste the nucleotide sequence in the Primer design Template section and get the set of primers just clicking Pick primers.</b></p>,""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        con1 = st.container(border=True)
        tid = con1.text_input("Enter the Gene ID: ", placeholder="e.g., Ca_00001", key="ginfo_Tid_input1").strip()
        mtid = con1.text_input("Enter multiple Gene IDs: ", placeholder="e.g., Ca_00001, Ca_00002", key="ginfo_mTid_input2").strip()
        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)

    with col2:
        con2 = st.container(border=True)
        locid = con2.text_input("Enter the NCBI ID: ", placeholder="e.g., LOC101511858", key="ginfo_Locid_input1").strip()
        mlocid = con2.text_input("Enter multiple NCBI IDs: ", placeholder="e.g., LOC101511858, LOC101496413", key="ginfo_mLocid_input2").strip()
        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)

    con1, con2, con3 = st.columns([2, 2, 2])
    with con2:
        start_button = st.button("Search", use_container_width=True, key="ginfo_Searchbutton1")

    if start_button:
        if tid:
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]

                if not matching_row.empty:
                    con=st.container(border=True)
                    with con:
                        st.subheader("Sequence data")
                        show_sequence_data_p(tid)

                        with st.expander("Primer Design", expanded=True):
                            st.markdown("""<div style='display: flex; justify-content: center;'><iframe src="https://www.primer3plus.com/" width="900" height="700" style="border:none;"></iframe></div>""", unsafe_allow_html=True)

                else:
                    st.error(f"No match found for Gene ID: {tid}")

            st.toast("Task completed successfully.")
            
        elif mtid:
            mtid_list = [tid.strip() for tid in mtid.replace(",", " ").split()]
            mtid_list.sort()

            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_rows = df[df['Transcript id'].isin(mtid_list)]
                found_ids = matching_rows['Transcript id'].unique().tolist()
                not_found_ids = [x for x in mtid_list if x not in found_ids]

                if not matching_rows.empty:
                    con = st.container(border=True)
                    with con:
                        st.subheader("\nSequences data")
                        show_sequence_data_p(mtid_list, is_multi=True)

                        with st.expander("Primer Design", expanded=True):
                            st.markdown("""<div style='display: flex; justify-content: center;'><iframe src="https://www.primer3plus.com/" width="900" height="700" style="border:none;"></iframe></div>""", unsafe_allow_html=True)


                if not_found_ids:
                    st.error(f"No matches found for Gene IDs: {', '.join(not_found_ids)}")

            st.toast("Task completed successfully.")
            
        elif locid:
            tid = process_locid(locid)
            if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                matching_row = df[df['Transcript id'] == tid]

                if not matching_row.empty:
                    con=st.container(border=True)
                    with con:
                        st.subheader("Sequence data")
                        show_sequence_data_p(tid)

                        with st.expander("Primer Design", expanded=True):
                            st.markdown("""<div style='display: flex; justify-content: center;'><iframe src="https://www.primer3plus.com/" width="900" height="700" style="border:none;"></iframe></div>""", unsafe_allow_html=True)


                else:
                    st.error(f"No match found for NCBI ID: {locid}")
            
            st.toast("Task completed successfully.")
            
        elif mlocid:
            available, rejected = mlocid_error(mlocid)
            if available:
                mtid = process_mlocid(",".join(available))
                mtid_list = [x.strip() for x in mtid.replace(",", " ").split()]
                mtid_list.sort()
                if 'Transcript id' in df.columns and 'lncRNA' in df.columns:
                    matching_rows = df[df['Transcript id'].isin(mtid_list)]
                    if not matching_rows.empty:
                        con = st.container(border=True)
                        with con:
                            st.subheader("\nSequences data")
                            show_sequence_data_p(mtid_list, is_multi=True)

                            with st.expander("Primer Design", expanded=True):
                                st.markdown("""<div style='display: flex; justify-content: center;'><iframe src="https://www.primer3plus.com/" width="900" height="700" style="border:none;"></iframe></div>""", unsafe_allow_html=True)


                st.toast("Task completed successfully.")
            if rejected:
                st.error(f"No matches found for NCBI IDs: {', '.join(rejected)}")

            st.toast("Task completed successfully.")
            
    elif tid == "":
        st.warning("Need Gene ID to proceed.")
    else:
        st.write("Press the 'Search' button to begin ...")
        st.write("Follow the instructions or check out tutorials")

    base_footer()
    return
