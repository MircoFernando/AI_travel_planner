

import json
from openai import OpenAI
from datetime import datetime

# OOP Implementation of Travel Planner\

# Fix validations

class Destination:
    def __init__(self, city, country, start_date, end_date, budget, activities):
        self.city = city
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.budget = float(budget)
        self.activities = activities

    def update_details(self, city=None, country=None, start_date=None, end_date=None, budget=None, activities=None):
        if city:
            self.city = city
        if country:
            self.country = country
        if start_date:
            self.start_date = start_date
        if end_date:
            self.end_date = end_date
        if budget:
            self.budget = float(budget)
        if activities:
            self.activities = activities

    def __str__(self):
        return (
            f"📍 {self.city}, {self.country}\n"
            f"   Dates: {self.start_date} to {self.end_date}\n"
            f"   Budget: ${self.budget:.2f}\n"
            f"   Activities: {', '.join(self.activities)}"
        )

    def to_dict(self):
        return {
            "city": self.city,
            "country": self.country,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "budget": self.budget,
            "activities": self.activities
        }
    
    def validate(self):
        if not self.city or not self.country:
            raise ValueError("City and country must be specified.")
        if not self.start_date or not self.end_date:
            raise ValueError("Start and end dates must be specified.")
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        if start >= end:
            raise ValueError("Start date must be before end date.")
        if self.budget <= 0:
            raise ValueError("Budget must be a positive number.")
        if not self.activities:
            raise ValueError("At least one activity must be specified.")

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["city"],
            data["country"],
            data["start_date"],
            data["end_date"],
            data["budget"],
            data["activities"]
        )
    
class AITravelAssistant:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)  

    def generate_itinerary(self, destination):
        prompt = f"""
        Create a day-by-day travel itinerary for a trip to {destination.city}, {destination.country}
        from {destination.start_date} to {destination.end_date}.
        Budget: {destination.budget} USD.
        Preferred activities: {', '.join(destination.activities)}.
        The plan should be practical and exciting.
        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel planner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    def generate_budget_tips(self, destination):
        prompt = f"""
        Provide budget-saving travel tips for a trip to {destination.city}, {destination.country}
        from {destination.start_date} to {destination.end_date}.
        Budget: {destination.budget} USD.
        Activities: {', '.join(destination.activities)}.
        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel planner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content



    
    
class ItineryManager:
    def __init__(self):
        self.destinations = []

    def add_destination(self, destination):
        self.destinations.append(destination)

    def remove_destination(self, city):
        for destination in self.destinations:
            if destination.city == city:
                self.destinations.remove(destination)
                break
            if destination.city != city:
                print(f"Destination {city} not found.")
                break

    def update_destination(self, city, **kwargs):
        for destination in self.destinations:
            if destination.city == city:
                destination.update_details(**kwargs)
                print(f"You have successfully updated your Destination: {destination}")
                break
        


    def search_destination(self, city):
        for destination in self.destinations:
            if destination.city == city:
                return destination
            
            print(f"Destination {city} not found.")
            break
    
    def view_all_destinations(self):
        for destination in self.destinations:
            print(destination)
        
    def save_iternary(self, filename="iternaries.json"):
        try:
            with open(filename, "w") as f:
                json.dump([d.to_dict() for d in self.destinations], f, indent=4)
            print(f"Itinerary saved to {filename}")
        except Exception as e:
            print(f"Error saving itinerary: {e}")
    
    def load_iternary(self, filename="iternaries.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.destinations = [Destination.from_dict(d) for d in data]
        except FileNotFoundError:
            print(f"No itinerary file found at {filename}.")

    def sort_destinations(self, key="budget"):
        if key == "budget":
            self.destinations.sort(key=lambda d: d.budget)
        elif key == "start_date":
            self.destinations.sort(key=lambda d: d.start_date)
        elif key == "end_date":
            self.destinations.sort(key=lambda d: d.end_date)
        else:
            print("Invalid sort key. Please use 'budget', 'start_date', or 'end_date'.")
            return
         
        for destination in self.destinations:
            print(destination)
        
        print("Destinations sorted successfully.")
    

    def choice_input(self):

        choice = input(
    "1. Add Destination\n"
    "2. Remove Destination\n"
    "3. Update Destination\n"
    "4. Search Destination\n"
    "5. View All Destinations\n"
    "6. AI Travel Assistance\n"
    "7. Save Itinerary\n"
    "8. Load Itinerary\n"
    "9. Sort Destinations\n"
    "10. Exit\n"
    "Enter your choice: "
    )
        return choice
    
    def display_menu(self, choice, ai_assistant):
        
        if choice == "1":
                city = input("Enter city: ")
                country = input("Enter country: ")
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                try:
                    budget = float(input("Enter budget: "))
                except ValueError as e:
                    print(f"Error: {e}")
                activities = input("Enter activities (comma separated): ").split(",")
                new_dest = Destination(city, country, start_date, end_date, budget, activities)
                try:
                    new_dest.validate()
                    self.add_destination(new_dest)
                    print(f"Added destination: {new_dest}")
                except ValueError as e:
                    print(f"Error: {e}")
                
        elif choice == "2":
                city = input("Enter city to remove: ")
                self.remove_destination(city)
                print(f"Removed destination: {city}")

        elif choice == "3":
            city = input("Enter city to update: ")
            print("What do you want to update?")
            update_choice = input(
                "1. Start Date\n"
                "2. End Date\n"
                "3. Budget\n"
                "4. Activities\n"
                "Enter your choice: "
            )
            if update_choice == "1":
                new_start_date = input("Enter new Start Date: ")
                self.update_destination(city, start_date=new_start_date)
            elif update_choice == "2":
                new_end_date = input("Enter new End Date: ")
                self.update_destination(city, end_date=new_end_date)
            elif update_choice == "3":
                try:
                    new_bugdet = float(input("Enter new Bugdet: "))
                    self.update_destination(city, budget=new_bugdet)
                except ValueError as e:
                    print(f"Error: {e}") 
            elif update_choice == "4":
                new_activities = input("Enter new Activites: ").split(",")
                self.update_destination(city, activities=new_activities)

        elif choice == "4":
            search_city = input("Enter a City: ")
            self.search_destination()
            if destination:
                print(destination)

        elif choice == "5":
            self.view_all_destinations()

            
        elif choice == "6":
            city = input("Enter city to get AI suggestions: ")
            destination = self.search_destination(city)
            if destination:
                print("----- Suggested Itinerary -----")
                print(ai_assistant.generate_itinerary(destination))

                print("----- Budget Tips -----")
                print(ai_assistant.generate_budget_tips(destination))
            else:
                print(f"No destination found for {city}.")
                
        elif choice == "7":
            self.save_iternary()
            print("Itinerary saved successfully.")

        elif choice == "8":
            self.load_iternary()
            print("Itinerary loaded successfully.")
        
        elif choice == "9":
            sort_key = input("Sort by (budget/start_date/end_date): ").strip().lower()
            self.sort_destinations(sort_key)
        
        elif choice == "10":
            print("Exiting the AI Travel Planner. Safe travels!")
            exit()


        if choice not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("Invalid choice. Please try again.")

    def init(self):

        dest1 =  Destination("Paris", "France", "2025-08-10", "2025-08-15", 1200, ["Eiffel Tower", "Louvre Museum"])
        dest2 = Destination("Tokyo", "Japan", "2025-09-01", "2025-09-07", 1800, ["Shinjuku", "Mount Fuji Tour"])

        self.add_destination(dest1)
        self.add_destination(dest2)

        ai_assistant = AITravelAssistant(api_key="OPENAI_API_KEY")

        while True:
            print("\n--- Welcome to the AI Travel Planner ---")
            print("Please select an option:")
            input_choice = self.choice_input()
            self.display_menu(input_choice, ai_assistant)
        



def main():
    manager = ItineryManager()

    

    manager.init()
 
main() 