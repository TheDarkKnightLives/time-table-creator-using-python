import random
import os 
class Timetable:
    def __init__(self):
        self.theory_subjects = {}
        self.lab_subjects = {}

    def add_theory_subject(self, name, hours, is_static, schedule=None):
        self.theory_subjects[name] = {'hours': hours, 'static': is_static, 'schedule': schedule}

    def add_lab_subject(self, name, hours, session, days):
        self.lab_subjects[name] = {'hours': hours, 'session': session, 'days': days}

    def display_timetable(self):
        print("\nTheory Subjects:")
        for name, details in self.theory_subjects.items():
            static_status = "Static" if details['static'] else "Non-static"
            print(f"{name}: {details['hours']} hours, {static_status}")
            if details['static']:
                print(f"  Schedule: {details['schedule']}")
        
        print("\nLab Subjects:")
        for name, details in self.lab_subjects.items():
            print(f"{name}: {details['hours']} hours, {details['session']}")

    def generate_fake_timetable(self):
        days = {day: ["empty"] * 5 for day in range(1, 7)}

        # Update timetable with static periods for theory subjects
        for name, details in self.theory_subjects.items():
            if details['static']:
                for day, periods in details['schedule'].items():
                    for period in periods:
                        if 1 <= period <= 5:  # Ensure the period is within the timetable slots
                            days[day][period - 1] = name

        # Update timetable with lab subjects based on session
        for lab_name, lab_details in self.lab_subjects.items():
            hours = lab_details['hours']
            session = lab_details['session']
            days_with_lab = lab_details['days']

            for day in days_with_lab:
                if session == "forenoon":
                    # Fill forenoon slots (periods 1-3)
                    periods = min(hours, 3)
                    for i in range(periods):
                        if days[day][i] == "empty":
                            days[day][i] = lab_name
                        hours -= 1
                        if hours == 0:
                            break
                elif session == "afternoon":
                    # Fill afternoon slots (periods 4-5) for 2-hour labs
                    if hours == 2:
                        for i in range(3, 5):  # Periods 4, 5 are index 3, 4
                            if days[day][i] == "empty":
                                days[day][i] = lab_name
                                hours -= 1
                                if hours == 0:
                                    break
                    else:
                        # Handle other cases if needed
                        for i in range(2, 5):  # Periods 3, 4, 5 are index 2, 3, 4
                            if days[day][i] == "empty":
                                days[day][i] = lab_name
                                hours -= 1
                                if hours == 0:
                                    break

        # Fill remaining periods with non-static theory subjects
        non_static_subjects = [name for name, details in self.theory_subjects.items() if not details['static']]
        for day, periods in days.items():
            empty_slots = [i for i, period in enumerate(periods) if period == "empty"]
            if empty_slots:
                random.shuffle(non_static_subjects)  # Shuffle to randomize the selection
                subject_index = 0
                for slot in empty_slots:
                    if subject_index >= len(non_static_subjects):
                        break
                    periods[slot] = non_static_subjects[subject_index]
                    subject_index += 1

        return days

def get_theory_subjects():
    theory_subjects = {}
    
    while True:
        try:
            num_theory = int(input("Enter the number of theory subjects: "))
            if num_theory <= 0:
                raise ValueError("Number of subjects must be positive.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a positive integer.")
    
    for _ in range(num_theory):
        while True:
            try:
                name = input("Enter the name of the theory subject: ").strip()
                if not name:
                    raise ValueError("Subject name cannot be empty.")
                
                hours = int(input(f"Enter the number of hours for {name}: "))
                if hours <= 0:
                    raise ValueError("Hours must be positive.")
                
                is_static = input(f"Is {name} static? (yes/no): ").lower()
                if is_static not in ['yes', 'no']:
                    raise ValueError("Please enter 'yes' or 'no'.")
                is_static = is_static == 'yes'
                
                schedule = None
                if is_static:
                    schedule = {}
                    remaining_hours = hours
                    while remaining_hours > 0:
                        try:
                            day = int(input(f"Enter day number (1-6) for the next hour of {name}: "))
                            if day not in range(1, 7):
                                raise ValueError("Day number must be between 1 and 6.")
                            
                            periods = input(f"Enter periods for {name} on day {day} (comma-separated): ").split(',')
                            periods = [int(period) for period in periods if period.isdigit()]
                            
                            if len(periods) > remaining_hours:
                                raise ValueError(f"You cannot enter more than {remaining_hours} periods.")
                            
                            schedule.setdefault(day, []).extend(periods)
                            remaining_hours -= len(periods)
                            print(f"{remaining_hours} hour(s) left.")
                            
                            if remaining_hours > 0:
                                print("Please provide periods for the remaining hours.")
                        except ValueError as e:
                            print(f"Invalid input: {e}. Please try again.")
                
                theory_subjects[name] = {'hours': hours, 'static': is_static, 'schedule': schedule}
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")
    
    return theory_subjects

def get_lab_subjects():
    lab_subjects = {}
    
    while True:
        try:
            num_lab = int(input("Enter the number of lab subjects: "))
            if num_lab <= 0:
                raise ValueError("Number of subjects must be positive.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a positive integer.")
    
    for _ in range(num_lab):
        while True:
            try:
                name = input("Enter the name of the lab subject: ").strip()
                if not name:
                    raise ValueError("Subject name cannot be empty.")
                
                hours = int(input(f"Enter the number of hours for {name}: "))
                if hours <= 0:
                    raise ValueError("Hours must be positive.")
                
                days = []
                while not days:
                    try:
                        days_input = input(f"Enter the day numbers (comma-separated) for {name}: ").split(',')
                        days = [int(day) for day in days_input if day.isdigit() and 1 <= int(day) <= 6]
                        if not days:
                            raise ValueError("Day numbers must be between 1 and 6.")
                    except ValueError as e:
                        print(f"Invalid input: {e}. Please enter valid day numbers.")
                
                session = input(f"Is {name} scheduled for forenoon or afternoon? ").lower()
                if session not in ['forenoon', 'afternoon']:
                    raise ValueError("Please enter 'forenoon' or 'afternoon'.")
                
                lab_subjects[name] = {'hours': hours, 'session': session, 'days': days}
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")
    
    return lab_subjects

def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

def main():
    timetable = Timetable()

    print("Enter theory subjects details:")
    theory_subjects = get_theory_subjects()

    print("\nEnter lab subjects details:")
    lab_subjects = get_lab_subjects()

    for name, details in theory_subjects.items():
        timetable.add_theory_subject(name, details['hours'], details['static'], details.get('schedule'))

    for name, details in lab_subjects.items():
        timetable.add_lab_subject(name, details['hours'], details['session'], details['days'])

    timetable.display_timetable()
    
    satisfied = False
    while not satisfied:
        print("\nGenerating fake timetable...")
        fake_timetable = timetable.generate_fake_timetable()

        print("\nFake Timetable:")
        for day, periods in fake_timetable.items():
            formatted_periods = []
            for i, period in enumerate(periods):
                if period == "empty":
                    formatted_periods.append("empty")
                else:
                    formatted_periods.append(period)
            formatted_timetable = " ".join(formatted_periods)
            print(f"Day {day}: {formatted_timetable}")

        response = input("\nAre you satisfied with the timetable? type (yes) or (just hit enter): ").strip().lower()
        if response == 'yes':
            satisfied = True
            clear_screen()
            print("Final Timetable:")
            for day, periods in fake_timetable.items():
                formatted_timetable = " ".join(periods)
                print(f"Day {day}: {formatted_timetable}")
        elif response == 'no':
            print("Shuffling and generating a new timetable...\n")

if __name__ == "__main__":
    main()