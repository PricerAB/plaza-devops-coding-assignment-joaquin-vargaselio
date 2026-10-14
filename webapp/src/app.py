import requests
import os
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

HELLO_WORLD_MESSAGE = os.environ.get("HELLO_WORLD_MESSAGE", "Hello from default app! (callback)")

@app.get("/")
def hello():
    return {"message": HELLO_WORLD_MESSAGE}

@app.get("/data")
def get_star_wars_data(id: int = Query(1, description="ID of the Star Wars character")):
    try:
        # FEATURE 2 CHANGE: Replaced hard-coded "1" with the dynamic query parameter `id`
        response = requests.get(f"https://swapi.info/api/people/{id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Character not found")
        raise HTTPException(status_code=500, detail="API Error")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Service Unavailable")
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=500, detail="Data Processing Error")


# FEATURE 3: Added new endpoint to return the top 20 people with the highest BMI
@app.get("/top-people-by-bmi")
def get_top_people_by_bmi():
    try:
        response = requests.get("https://swapi.info/api/people", timeout=10)
        response.raise_for_status()
        people = response.json()
        
        valid_people = []
        for person in people:
            try:
                mass_str = person.get("mass", "unknown")
                height_str = person.get("height", "unknown")
                
                if mass_str == "unknown" or height_str == "unknown":
                    continue
                    
                mass = float(mass_str)
                height_cm = float(height_str)
                
                if height_cm <= 0:
                    continue
                
                height_m = height_cm / 100.0
                
                bmi = mass / (height_m ** 2)
                
                person_data = person.copy()
                person_data["bmi"] = round(bmi, 2)
                valid_people.append(person_data)
                
            except (ValueError, TypeError):
                continue
                
        sorted_people = sorted(valid_people, key=lambda x: x["bmi"], reverse=True)
        
        return sorted_people[:20]

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Service Unavailable from SWAPI")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
