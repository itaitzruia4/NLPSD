from stats import Statistics
import pickle

def main():
    stats = Statistics()
    
    min_knesset_num = 24
    max_knesset_num = 25

    # get all warnings
    sessions2warnings = dict()
    for knesset_num in range(min_knesset_num, max_knesset_num + 1):
        for category_id in stats.knesset_categories_sessions[knesset_num]:
            if category_id == 6:
                continue
            with open(f'results/warnings_finetune_{knesset_num}_{category_id}.pkl', 'rb') as f:
                warnings = pickle.load(f)
            filtered_warnings = {session_id: warnings[session_id][0] for session_id in warnings}
            sessions2warnings.update(filtered_warnings)
    warns_per_knes = stats.warnings_per_knesset_num(sessions2warnings)

    for kns_num, warns in warns_per_knes[0].items():
        top_warnings = sorted(warns.items(), key=lambda x: sum(x[1]), reverse=True)[:3]
        print("knesset number: ", kns_num)
        print("top warnings: ", top_warnings)

    

if __name__ == '__main__':
    main()