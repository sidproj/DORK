from datetime import datetime,timezone as dt_timezone
from zoneinfo import ZoneInfo

class DateTimeTool:
    name = "datetime"
    
    description = (
        "Get the current date and time"
        "Can return the current local time, UTC time"
        "or the current time in a specified IANA timezone"
    )
    
    parameters = {
        "type":"object",
        "properties":{
            "timezone":{
                "type":"string",
                "description":(
                     "IANA timezone such as "
                    "'Asia/Kolkata', 'America/New_York', "
                    "or 'Europe/London'. "
                    "Use 'UTC' for UTC time."
                )
            }
        },
        "required":["timezone"]
    }
    
    @staticmethod
    def definition():
        return {
            "type":"function",
            "function":{
                "name":DateTimeTool.name,
                "description":DateTimeTool.description,
                "parameters":DateTimeTool.parameters
            }
        }
    
    @staticmethod
    def execute(timezone: str):
        try:
            if timezone.upper() == "UTC":
                now = datetime.now(dt_timezone.utc)
            else:
                now = datetime.now(ZoneInfo(timezone))

            return {
                "datetime":now.isoformat(),
                "date":now.strftime("%Y-%m-%d"),
                "time":now.strftime("%H:%M:%S")
            }
        except Exception as e:
            print(e)
            raise ValueError(
                f"Invalid timezone: {timezone}"
            )