from langchain_core.tools import tool
import requests
from pydantic import BaseModel, Field

@tool
def Get_Hotel_Room_Vacancies(
    hotel_group_types: str,
    check_in: str,
    check_out: str,
    adults: int,
    children: int,
    lowest_price: int,
    highest_price: int,
    county_ids: list,
    district_ids: list,
    hotel_facility_ids: list,
    room_types: list,
    room_facility_ids: list,
    has_breakfast: bool,
    has_lunch: bool,
    has_dinner: bool
):
    """
    多條件過濾可預訂旅館空房
    
    * args:
        - hotel_group_types (str): 旅館類別
        - check_in (str): 退房日期 (ex. 2025-01-01)
        - check_out (str): 退房日期 (ex. 2025-01-03)
        - adults (int): 成人數
        - children (int): 兒童數
        - lowest_price (int): 最低價格
        - highest_price (int): 最高價格
        - county_ids[] (list): 城市 ID 列表
        - district_ids[] (list): 鄉鎮區 ID 列表
        - hotel_facility_ids[] (list): 旅館設施 ID 列表
        - room_types[] (list): 房型 ID 列表
        - room_facility_ids[] (list): 房間設施 ID 列表
        - has_breakfast (bool): 是否有早餐
        - has_lunch (bool): 是否有午餐
        - has_dinner (bool): 是否有晚餐
    * returns:
        - List of room vacancy objects
    """
    
    url = f"https://k6oayrgulgb5sasvwj3tsy7l7u0tikfd.lambda-url.ap-northeast-1.on.aws/api/v3/tools/interview_test/taiwan_hotels/hotel/vacancies?hotel_group_types={hotel_group_types}&check_in={check_in}&check_out={check_out}&adults={adults}&children={children}&lowest_price={lowest_price}&highest_price={highest_price}&county_ids={county_ids}&district_ids={district_ids}&hotel_facility_ids={hotel_facility_ids}&room_types={room_types}&room_facility_ids={room_facility_ids}&has_breakfast={has_breakfast}&has_lunch={has_lunch}&has_dinner={has_dinner}"
    
    headers = {
        "accept": "application/json",
        "Authorization": "DhDkXZkGXaYBZhkk1Z9m9BuZDJGy"
    }

    response = requests.get(url, headers=headers)
    return response.text

@tool
def Get_Plans():
    """
    取得旅館訂購方案
    
    * args:
        - hotel_keyword (str): 旅館名稱/關鍵字
        - plan_keyword (str): 旅館訂購方案名稱/關鍵字
        - check_in_start_at (str): 退房日期 (ex. 2025-01-01)
        - check_in_end_at (str): 退房日期 (ex. 2025-01-03)
    * returns:
        - List of plans
    """
    
    url = f"https://k6oayrgulgb5sasvwj3tsy7l7u0tikfd.lambda-url.ap-northeast-1.on.aws/api/v3/tools/interview_test/taiwan_hotels/plans?hotel_keyword={hotel_keyword}&plan_keyword={plan_keyword}&check_in_start_at={check_in_start_at}&check_in_end_at={check_in_end_at}"

    headers = {
        "accept": "application/json",
        "Authorization": "DhDkXZkGXaYBZhkk1Z9m9BuZDJGy"
    }

    response = requests.get(url, headers=headers)

    return response.text

@tool
def Get_Hotel_Details():
    """
    取得旅館詳細資訊
    
    * args:
        - hotel_id (str): 旅館 ID
    * returns:
        - The most similar hotel object
    """
    url = f"https://k6oayrgulgb5sasvwj3tsy7l7u0tikfd.lambda-url.ap-northeast-1.on.aws/api/v3/tools/interview_test/taiwan_hotels/hotel/details?hotel_id={hotel_id}"

    headers = {
        "accept": "application/json",
        "Authorization": "DhDkXZkGXaYBZhkk1Z9m9BuZDJGy"
    }

    response = requests.get(url, headers=headers)
    return response.text


@tool
def Guess_Hotel():
    """
    取得旅館名稱模糊匹配
    
    * args:
        - hotel_name (str): 旅館名稱
    * returns:
        - The most similar hotel object
    """
    
    url = f"https://k6oayrgulgb5sasvwj3tsy7l7u0tikfd.lambda-url.ap-northeast-1.on.aws/api/v3/tools/interview_test/taiwan_hotels/hotel/fuzzy_match?hotel_name={hotel_name}"

    headers = {
        "accept": "application/json",
        "Authorization": "DhDkXZkGXaYBZhkk1Z9m9BuZDJGy"
    }

    response = requests.get(url, headers=headers)
    return response.text

@tool
def Get_Hotels():
    """
    取得指定類型之旅館列表
    
    * args:
        - hotel_group_types (str): 旅館類型
    * returns:
        - List of hotels
    """
    
    url = f"https://k6oayrgulgb5sasvwj3tsy7l7u0tikfd.lambda-url.ap-northeast-1.on.aws/api/v3/tools/interview_test/taiwan_hotels/hotels?hotel_group_types={hotel_group_types}"

    headers = {
        "accept": "application/json",
        "Authorization": "DhDkXZkGXaYBZhkk1Z9m9BuZDJGy"
    }

    response = requests.get(url, headers=headers)
    return response.text


@tool
def Get_Hotel_Room_Types():
    """
    取得旅館房間類型列表
    
    * args: None
    * returns:
        - List of hotel room type ids and names
    """
    
    url = f"https://k6oayrgulgb5sasvwj3tsy7l7u0tikfd.lambda-url.ap-northeast-1.on.aws/api/v3/tools/interview_test/taiwan_hotels/hotel/room_type/room_types?page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "DhDkXZkGXaYBZhkk1Z9m9BuZDJGy"
    }

    response = requests.get(url, headers=headers)
    return response.text

@tool
def Get_Hotel_Room_Type_Facilities():
    """
    取得旅館房間設施列表
    
    * args: None
    * returns:
        - List of hotel room type facility ids and names
    """
    
    url = f"https://k6oayrgulgb5sasvwj3tsy7l7u0tikfd.lambda-url.ap-northeast-1.on.aws/api/v3/tools/interview_test/taiwan_hotels/hotel/room_type/facilities?page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "DhDkXZkGXaYBZhkk1Z9m9BuZDJGy"
    }

    response = requests.get(url, headers=headers)
    return response.text

@tool
def Get_Hotel_Facilities():
    """
    取得旅館設施列表
    
    * args: None
    * returns:
        - List of hotel facility ids and names
    """
    
    url = f"https://k6oayrgulgb5sasvwj3tsy7l7u0tikfd.lambda-url.ap-northeast-1.on.aws/api/v3/tools/interview_test/taiwan_hotels/hotel/facilities?page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "DhDkXZkGXaYBZhkk1Z9m9BuZDJGy"
    }

    response = requests.get(url, headers=headers)
    return response.text

@tool
def Get_Hotel_Group_Types():
    """
    取得台灣旅館館型列表
    
    * args: None
    * returns:
        - List of hotel group type names
    """
    
    url = f"https://k6oayrgulgb5sasvwj3tsy7l7u0tikfd.lambda-url.ap-northeast-1.on.aws/api/v3/tools/interview_test/taiwan_hotels/hotel_group/types?page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "DhDkXZkGXaYBZhkk1Z9m9BuZDJGy"
    }

    response = requests.get(url, headers=headers)
    return response.text


@tool
def Get_Districts():
    """
    取得台灣旅館鄉鎮區列表
    
    * args: None
    * returns:
        - List of district ids and names
    """
    
    url = f"https://k6oayrgulgb5sasvwj3tsy7l7u0tikfd.lambda-url.ap-northeast-1.on.aws/api/v3/tools/interview_test/taiwan_hotels/districts?page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "DhDkXZkGXaYBZhkk1Z9m9BuZDJGy"
    }

    response = requests.get(url, headers=headers)
    return response.text


@tool
def Get_Counties():
    """
    取得台灣旅館縣市列表
    
    * args: None
    * returns:
        - List of county ids and names
    """
    
    url = f"https://k6oayrgulgb5sasvwj3tsy7l7u0tikfd.lambda-url.ap-northeast-1.on.aws/api/v3/tools/interview_test/taiwan_hotels/counties?page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "DhDkXZkGXaYBZhkk1Z9m9BuZDJGy"
    }

    response = requests.get(url, headers=headers)
    return response.text

tool_box = [
    Get_Hotel_Room_Vacancies,
    Get_Plans,
    Get_Hotel_Details,
    Guess_Hotel,
    Get_Hotels,
    Get_Hotel_Room_Types,
    Get_Hotel_Room_Type_Facilities,
    Get_Hotel_Facilities,
    Get_Hotel_Group_Types,
    Get_Districts,
    Get_Counties,
    Get_Hotel_Room_Vacancies,
]