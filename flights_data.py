from sqlalchemy import create_engine, text

QUERY_FLIGHT_BY_ID = ("SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY "
                      "FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.ID = :id")

QUERY_FLIGHT_BY_DATE = ("SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY "
                        "FROM flights JOIN airlines ON flights.airline = airlines.id "
                        "WHERE flights.YEAR = :year AND flights.MONTH = :month AND flights.DAY = :day")

QUERY_DELAYED_FLIGHT_BY_AIRLINE = (
    "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY "
    "FROM flights JOIN airlines ON flights.airline = airlines.id "
    "WHERE airlines.AIRLINE = :airline  AND flights.DEPARTURE_DELAY > 20")

QUERY_DELAYED_FLIGHT_BY_AIRPORT = (
    "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY "
    "FROM flights JOIN airlines ON flights.airline = airlines.id "
    "WHERE flights.ORIGIN_AIRPORT = upper(:origin_airport) AND flights.DEPARTURE_DELAY > 20")

# Define the database URL
DATABASE_URL = "sqlite:///data/flights.sqlite3"

# Create the engine
engine = create_engine(DATABASE_URL)


def execute_query(query, params):
    """
    Execute an SQL query with the params provided in a dictionary,
    and returns a list of records (dictionary-like objects).
    If an exception was raised, print the error, and return an empty list.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            return result.fetchall()

    except Exception as e:
        print("Query error:", e)
        return []


def get_flight_by_id(flight_id):
    """
    Searches for flight details using flight ID.
    If the flight was found, returns a list with a single record.
    """
    params = {'id': flight_id}
    return execute_query(QUERY_FLIGHT_BY_ID, params)


def get_flights_by_date(day, month, year):
    """
    Searches for flight details using flight date.
    If the flight was found, returns a list with a single record.
    """
    params = {'year': year, 'month': month, 'day': day}
    return execute_query(QUERY_FLIGHT_BY_DATE, params)


def get_delayed_flights_by_airport(origin_airport):
    """
    Searches for flight details using flight origin airport.
    If the flight was found, returns a list with a single record.
    """
    params = {'origin_airport': origin_airport}
    return execute_query(QUERY_DELAYED_FLIGHT_BY_AIRPORT, params)


def get_delayed_flights_by_airline(airline):
    """
    Searches for flight details using flight airline.
    If the flight was found, returns a list with a single record.
    """
    params = {'airline': airline}
    return execute_query(QUERY_DELAYED_FLIGHT_BY_AIRLINE, params)
