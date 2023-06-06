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
            with open(f'results/warnings_finetune_{knesset_num}_{category_id}.pkl', 'rb') as f:
                warnings = pickle.load(f)
                filtered_warnings = {session_id: warnings[session_id][0] for session_id in warnings}
                sessions2warnings.update(filtered_warnings)

    

if __name__ == '__main__':
    main()