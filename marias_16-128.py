import streamlit as st
import pandas as pd

# ===== Základní rozlosovací klíče =====
SEATING_KEYS = {
    16: [
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
        [[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]],
        [[1, 6, 11, 16], [2, 5, 12, 15], [3, 8, 9, 14], [4, 7, 10, 13]],
        [[1, 7, 12, 14], [2, 8, 11, 13], [3, 5, 10, 16], [4, 6, 9, 15]],
        [[1, 8, 10, 15], [2, 7, 9, 16], [3, 6, 12, 13], [4, 5, 11, 14]]
    ],
    20: [
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19, 20]],
        [[1, 5, 9, 13], [2, 6, 10, 17], [3, 7, 14, 18], [4, 11, 15, 19], [8, 12, 16, 20]],
        [[1, 6, 15, 20], [2, 5, 12, 18], [3, 9, 16, 19], [4, 7, 10, 13], [8, 11, 14, 17]],
        [[1, 10, 16, 18], [2, 8, 13, 19], [3, 5, 11, 20], [4, 6, 9, 14], [7, 12, 15, 17]],
        [[1, 12, 14, 19], [2, 7, 9, 20], [3, 8, 10, 15], [4, 5, 16, 17], [6, 11, 13, 18]]
    ],
    24: [
        [[1, 2, 11, 21], [9, 10, 19, 5], [17, 3, 18, 13], [4, 7, 6, 24], [8, 12, 14, 15], [16, 20, 22, 23]],
        [[1, 3, 12, 22], [9, 11, 20, 6], [17, 4, 19, 14], [5, 8, 7, 23], [2, 13, 15, 16], [10, 21, 24, 18]],
        [[1, 4, 13, 23], [9, 12, 21, 7], [17, 5, 20, 15], [6, 2, 8, 24], [3, 14, 16, 10], [11, 22, 18, 19]],
        [[1, 5, 14, 24], [9, 13, 22, 8], [17, 6, 21, 16], [7, 3, 2, 18], [4, 15, 10, 11], [12, 23, 19, 20]],
        [[1, 6, 15, 18], [9, 14, 23, 2], [17, 7, 22, 10], [8, 4, 3, 19], [5, 16, 11, 12], [13, 24, 20, 21]]
    ],
    28: [
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28]],
        [[1, 5, 9, 13], [2, 6, 10, 17], [3, 7, 11, 18], [4, 8, 12, 25], [14, 27, 19, 23], [16, 20, 21, 26], [22, 24, 15, 28]],
        [[1, 6, 11, 16], [2, 7, 12, 26], [3, 8, 13, 27], [4, 5, 10, 28], [17, 21, 22, 23], [18, 24, 25, 19], [14, 15, 9, 20]],
        [[1, 7, 16, 22], [2, 8, 10, 23], [3, 5, 11, 24], [4, 6, 12, 25], [13, 18, 20, 27], [14, 19, 21, 28], [15, 17, 9, 26]],
        [[1, 8, 11, 27], [2, 5, 12, 28], [3, 6, 10, 25], [4, 7, 13, 26], [14, 18, 21, 24], [15, 19, 20, 22], [16, 17, 23, 9]] 
    ]
}

# Manuální oprava SEATING_KEYS[28][0]
if not isinstance(SEATING_KEYS[28][0][-1], list):
    SEATING_KEYS[28][0] = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16], [17,18,19,20], [21,22,23,24], [25,26,27,28]]

def find_key_combination(total_players):
    if total_players % 4 != 0: 
        return None
    if total_players == 0:
        return []

    available_sizes = sorted(SEATING_KEYS.keys(), reverse=True)
    memo = {}

    def helper(remaining):
        if remaining == 0:
            return []
        if remaining < 0:
            return None
        if remaining in memo:
            return memo[remaining]

        best_combination = None
        
        for size in available_sizes:
            if remaining >= size:
                res = helper(remaining - size)
                if res is not None:
                    current_combination = [size] + res
                    if best_combination is None or len(current_combination) < len(best_combination):
                        best_combination = current_combination
        
        memo[remaining] = best_combination
        return best_combination

    return helper(total_players)

def build_seating_for_round(round_idx, key_combination, num_rounds_total):
    seating = []
    offset = 0
    for size in key_combination:
        round_keys = SEATING_KEYS[size]
        current_round_key_idx = round_idx % len(round_keys)
        
        for table in round_keys[current_round_key_idx]:
            adjusted_table = [player_id + offset for player_id in table]
            seating.append(adjusted_table)
        offset += size
    return seating

def find_duplicate_names(names_list):
    seen = set()
    duplicates = set()
    for name in names_list:
        if name == "": continue 
        if name in seen:
            duplicates.add(name)
        seen.add(name)
    return duplicates

def main():
    st.set_page_config(page_title="Mariášové turnaje Na Výsluní", layout="wide")
    
    # Inicializace session state
    if 'player_names' not in st.session_state:
        st.session_state.player_names = []
    if 'round_results_data' not in st.session_state:
        st.session_state.round_results_data = []
    if 'seating_data_cache' not in st.session_state:
        st.session_state.seating_data_cache = None
    if 'num_rounds' not in st.session_state:
        st.session_state.num_rounds = 0
    if 'current_round_for_results' not in st.session_state:
        st.session_state.current_round_for_results = 1
    
    st.title("Mariášové turnaje Na Výsluní")
    
    # Záložky aplikace
    tab1, tab2, tab3 = st.tabs(["Nastavení turnaje", "Rozlosování", "Výsledky"])
    
    with tab1:
        st.header("Nastavení turnaje")
        
        col1, col2 = st.columns(2)
        
        with col1:
            player_count = st.selectbox(
                "Počet hráčů:",
                options=list(range(16, 129, 4)),
                index=0,
                key="player_count"
            )
            
            num_rounds = st.number_input(
                "Počet kol:",
                min_value=1,
                max_value=20,
                value=5,
                step=1,
                key="num_rounds"
            )
            
            stake = st.number_input(
                "Výše vkladu (Kč):",
                min_value=1,
                value=10,
                step=1,
                key="stake"
            )
        
        with col2:
            st.subheader("Jména hráčů")
            
            # Dynamické generování vstupů pro jména hráčů
            player_names = []
            for i in range(player_count):
                default_name = f"Hráč {i+1}"
                if i < len(st.session_state.player_names):
                    default_name = st.session_state.player_names[i]
                name = st.text_input(
                    f"Hráč {i+1}:",
                    value=default_name,
                    key=f"player_name_{i}"
                )
                player_names.append(name)
            
            st.session_state.player_names = player_names
            
            duplicates = find_duplicate_names(player_names)
            if duplicates:
                st.error(f"Jména hráčů musí být unikátní. Duplicitní jména: {', '.join(duplicates)}")
            
            if "" in player_names:
                st.error("Všechna jména hráčů musí být vyplněna.")
    
    with tab2:
        st.header("Rozlosování hráčů")
        
        if st.button("Generovat rozlosování"):
            # Validace vstupů
            if "" in st.session_state.player_names:
                st.error("Nelze generovat rozlosování - některá jména hráčů nejsou vyplněna.")
                return
            
            duplicates = find_duplicate_names(st.session_state.player_names)
            if duplicates:
                st.error("Nelze generovat rozlosování - existují duplicitní jména hráčů.")
                return
            
            player_count = st.session_state.player_count
            key_combo = find_key_combination(player_count)
            
            if key_combo is None:
                st.error(f"Pro počet hráčů {player_count} nelze nalézt platnou kombinaci rozlosovacích klíčů.")
                return
            
            min_unique_rounds_for_combo = float('inf')
            for size in key_combo:
                min_unique_rounds_for_combo = min(min_unique_rounds_for_combo, len(SEATING_KEYS[size]))
            
            if st.session_state.num_rounds > min_unique_rounds_for_combo:
                st.warning(
                    f"Pro danou kombinaci hráčů je k dispozici {min_unique_rounds_for_combo} unikátních sad rozlosování. "
                    f"Požadujete {st.session_state.num_rounds} kol. Rozlosování se budou po {min_unique_rounds_for_combo} kolech opakovat."
                )
            
            st.session_state.seating_data_cache = [
                build_seating_for_round(r, key_combo, st.session_state.num_rounds) 
                for r in range(st.session_state.num_rounds)
            ]
            
            st.success("Rozlosování bylo úspěšně vygenerováno!")
        
        if st.session_state.seating_data_cache:
            st.subheader("Náhled rozlosování")
            
            round_to_show = st.selectbox(
                "Zobrazit kolo:",
                options=list(range(1, st.session_state.num_rounds + 1)),
                key="round_to_show"
            )
            
            round_idx = round_to_show - 1
            round_layout = st.session_state.seating_data_cache[round_idx]
            key_combo = []
            
            # Rekonstrukce key_combo z rozlosování
            if round_layout:
                max_player = max(max(table) for table in round_layout)
                key_combo = find_key_combination(max_player)
            
            group_offset = 0
            table_display_offset_in_round = 0
            
            for key_size in key_combo:
                st.markdown(f"**Skupina hráčů {group_offset + 1}-{group_offset + key_size}**")
                
                num_tables_in_group = key_size // 4
                tables_for_this_group = round_layout[table_display_offset_in_round : table_display_offset_in_round + num_tables_in_group]
                
                for table_idx_in_group, table_player_ids in enumerate(tables_for_this_group):
                    player_names_on_table = [st.session_state.player_names[player_id - 1] for player_id in table_player_ids]
                    
                    cols = st.columns(5)
                    cols[0].markdown(f"**Stůl {table_display_offset_in_round + table_idx_in_group + 1}:**")
                    for i, name in enumerate(player_names_on_table):
                        cols[i+1].markdown(name)
                
                table_display_offset_in_round += num_tables_in_group
                group_offset += key_size
            
            # Tlačítko pro export rozlosování
            seating_text = "=== Rozlosování připraveno ===\n\n"
            for r in range(st.session_state.num_rounds):
                seating_text += f"=== Kolo {r + 1} ===\n"
                round_layout = st.session_state.seating_data_cache[r]
                
                group_offset = 0
                table_display_offset_in_round = 0
                
                for key_size in key_combo:
                    seating_text += f"--- Skupina hráčů {group_offset + 1}-{group_offset + key_size} ---\n"
                    
                    num_tables_in_group = key_size // 4
                    tables_for_this_group = round_layout[table_display_offset_in_round : table_display_offset_in_round + num_tables_in_group]
                    
                    for table_idx_in_group, table_player_ids in enumerate(tables_for_this_group):
                        player_names_on_table = [st.session_state.player_names[player_id - 1] for player_id in table_player_ids]
                        seating_text += f"Stůl {table_display_offset_in_round + table_idx_in_group + 1}: {', '.join(player_names_on_table)}\n"
                    
                    table_display_offset_in_round += num_tables_in_group
                    group_offset += key_size
                
                seating_text += "\n"
            
            st.download_button(
                label="Stáhnout rozlosování jako TXT",
                data=seating_text,
                file_name="rozlosovani_turnaje.txt",
                mime="text/plain"
            )
    
    with tab3:
        st.header("Zadávání výsledků a pořadí")
        
        if not st.session_state.seating_data_cache:
            st.info("Nejprve vygenerujte rozlosování v záložce 'Rozlosování'.")
        else:
            st.session_state.current_round_for_results = st.selectbox(
                "Vyberte kolo pro zadání výsledků:",
                options=list(range(1, st.session_state.num_rounds + 1)),
                index=st.session_state.current_round_for_results - 1,
                key="current_round_select"
            )
            
            round_idx = st.session_state.current_round_for_results - 1
            round_layout = st.session_state.seating_data_cache[round_idx]
            
            # Inicializace výsledků pro toto kolo, pokud ještě neexistují
            if len(st.session_state.round_results_data) <= round_idx:
                st.session_state.round_results_data.extend([{} for _ in range(round_idx - len(st.session_state.round_results_data) + 1)])
            
            current_round_scores = st.session_state.round_results_data[round_idx]
            
            # Formulář pro zadávání výsledků
            with st.form(f"results_form_{round_idx}"):
                st.markdown(f"### Kolo {round_idx + 1}")
                
                for table_idx, table_players_indices in enumerate(round_layout):
                    st.markdown(f"**Stůl {table_idx + 1}**")
                    
                    cols = st.columns(4)
                    for i, player_id in enumerate(table_players_indices):
                        if player_id - 1 >= len(st.session_state.player_names):
                            continue
                        
                        player_name = st.session_state.player_names[player_id - 1]
                        
                        with cols[i]:
                            st.markdown(f"**{player_name}**")
                            
                            dokup = st.number_input(
                                "Dokup:",
                                min_value=0,
                                value=current_round_scores.get(player_name, {}).get('dokup_raw', 0),
                                key=f"dokup_{round_idx}_{table_idx}_{i}"
                            )
                            
                            nastole = st.number_input(
                                "Na stole:",
                                min_value=0,
                                value=current_round_scores.get(player_name, {}).get('nastole_raw', 0),
                                key=f"nastole_{round_idx}_{table_idx}_{i}"
                            )
                
                if st.form_submit_button("Uložit výsledky kola"):
                    # Validace a uložení výsledků
                    table_sums = {}
                    current_round_data_to_store = {}
                    
                    for table_idx, table_players_indices in enumerate(round_layout):
                        table_sum = 0
                        
                        for i, player_id in enumerate(table_players_indices):
                            if player_id - 1 >= len(st.session_state.player_names):
                                continue
                            
                            player_name = st.session_state.player_names[player_id - 1]
                            dokup = st.session_state[f"dokup_{round_idx}_{table_idx}_{i}"]
                            nastole = st.session_state[f"nastole_{round_idx}_{table_idx}_{i}"]
                            
                            player_score_for_round = nastole - (st.session_state.stake + dokup)
                            table_sum += player_score_for_round
                            
                            current_round_data_to_store[player_name] = {
                                'score': player_score_for_round,
                                'dokup_raw': dokup,
                                'nastole_raw': nastole
                            }
                        
                        table_sums[table_idx] = table_sum
                    
                    # Kontrola součtu na stolech
                    valid = True
                    for table_idx, total_score in table_sums.items():
                        if abs(total_score) > 1e-6:
                            st.error(f"Součet skóre u stolu {table_idx + 1} není 0 (je {total_score}). Zkontrolujte zadané hodnoty.")
                            valid = False
                    
                    if valid:
                        st.session_state.round_results_data[round_idx] = current_round_data_to_store
                        st.success("Výsledky kola byly úspěšně uloženy.")
            
            # Zobrazení konečného pořadí
            if st.button("Zobrazit konečné pořadí"):
                total_scores = {}
                all_rounds_empty = True
                
                for round_data in st.session_state.round_results_data:
                    if round_data:
                        all_rounds_empty = False
                        for player_name, score_details in round_data.items():
                            total_scores[player_name] = total_scores.get(player_name, 0) + score_details['score']
                
                if all_rounds_empty or not total_scores:
                    st.info("Nejsou k dispozici žádné výsledky kol pro zobrazení konečného pořadí.")
                else:
                    sorted_results = sorted(total_scores.items(), key=lambda item: item[1], reverse=True)
                    
                    st.subheader("Konečné pořadí")
                    
                    ranking_df = pd.DataFrame(
                        [(i+1, name, score) for i, (name, score) in enumerate(sorted_results)],
                        columns=["Pořadí", "Jméno hráče", "Celkové skóre (Kč)"]
                    )
                    
                    st.dataframe(
                        ranking_df,
                        hide_index=True,
                        use_container_width=True
                    )
                    
                    # Export výsledků
                    st.subheader("Export výsledků")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Export konečného pořadí
                        csv_ranking = ranking_df.to_csv(index=False, sep=";", encoding="utf-8-sig")
                        st.download_button(
                            label="Stáhnout konečné pořadí (CSV)",
                            data=csv_ranking,
                            file_name="konecne_poradi.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        # Export kompletních výsledků
                        player_list = st.session_state.player_names[:]
                        if not player_list:
                            all_players_in_results = set()
                            for rd in st.session_state.round_results_data:
                                all_players_in_results.update(rd.keys())
                            player_list = sorted(list(all_players_in_results))
                        
                        rounds_data = []
                        for round_idx, round_scores_dict in enumerate(st.session_state.round_results_data):
                            if round_scores_dict:
                                row_score = {"Typ": f"Kolo {round_idx + 1} - Skóre"}
                                for player_name in player_list:
                                    row_score[player_name] = round_scores_dict.get(player_name, {}).get('score', "-")
                                rounds_data.append(row_score)
                                
                                row_dokup = {"Typ": f"Kolo {round_idx + 1} - Dokupy"}
                                for player_name in player_list:
                                    row_dokup[player_name] = round_scores_dict.get(player_name, {}).get('dokup_raw', "-")
                                rounds_data.append(row_dokup)
                                
                                row_nastole = {"Typ": f"Kolo {round_idx + 1} - Na stole"}
                                for player_name in player_list:
                                    row_nastole[player_name] = round_scores_dict.get(player_name, {}).get('nastole_raw', "-")
                                rounds_data.append(row_nastole)
                        
                        if rounds_data:
                            rounds_df = pd.DataFrame(rounds_data)
                            csv_full = "Konečné pořadí hráčů\n" + ranking_df.to_csv(index=False, sep=";", lineterminator="\n")
                            csv_full += "\nPrůběh turnaje po kolech (Vklad na kolo: " + str(st.session_state.stake) + " Kč)\n"
                            csv_full += rounds_df.to_csv(index=False, sep=";", lineterminator="\n")
                            
                            st.download_button(
                                label="Stáhnout kompletní výsledky (CSV)",
                                data=csv_full,
                                file_name="kompletni_vysledky.csv",
                                mime="text/csv"
                            )

if __name__ == "__main__":
    main()