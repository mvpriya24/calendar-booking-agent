import datefinder
from calendar_utils import check_availability, book_slot

async def process_user_input(user_input):
    try:
        matches = list(datefinder.find_dates(user_input))

        if matches:
            parsed_datetime = matches[0]
            print(f"Parsed Datetime: {parsed_datetime}")

            suggested_time = parsed_datetime.strftime('%Y-%m-%dT%H:%M:%S')

            is_available = check_availability(suggested_time)
            if is_available:
                booking_link = book_slot(suggested_time)
                return f"✅ Booked your appointment for {parsed_datetime.strftime('%A, %d %B %Y at %I:%M %p')}! [View Event]({booking_link})"
            else:
                return f"❌ {parsed_datetime.strftime('%A, %d %B %Y at %I:%M %p')} is not available. Please try another time."
        else:
            return "❌ I couldn't understand the date and time. Please try again with a clearer format (e.g., 'Book a slot tomorrow at 4 PM' or 'Book for June 28 at 11 AM')."
    
    except Exception as e:
        print(f"Error in processing input: {e}")
        return "⚠️ Sorry, something went wrong while processing your request."
