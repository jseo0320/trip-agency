from datetime import time
from app.schemas.tourism import TouristPlaceResponse

PLACES = [
    TouristPlaceResponse(id=i, name=name, city=city, category=category, address=address,
        latitude=lat, longitude=lon, description=description, opening_time=time(9),
        closing_time=time(21), average_stay_minutes=stay, source="mock")
    for i, name, city, category, address, lat, lon, stay, description in [
        (1, "해운대 해수욕장", "busan", "sea", "부산 해운대구 해운대해변로", 35.1587,129.1604,90,"바다와 산책을 즐기는 부산의 대표 해변"),
        (2, "감천문화마을", "busan", "photo", "부산 사하구 감내2로",35.0975,129.0106,90,"언덕 위 다채로운 골목과 풍경"),
        (3, "광안리 해수욕장", "busan", "sea", "부산 수영구 광안해변로",35.1532,129.1186,90,"광안대교를 바라보는 해변"),
        (4, "전포 카페거리", "busan", "cafe", "부산 부산진구 전포대로",35.1556,129.0632,60,"골목마다 개성 있는 카페"),
        (5, "태화강 국가정원", "ulsan", "nature", "울산 중구 태화강국가정원길",35.5474,129.2874,100,"대나무 숲과 강변 산책"),
        (6, "대왕암공원", "ulsan", "sea", "울산 동구 등대로",35.4928,129.4427,90,"바다와 기암괴석을 잇는 산책로"),
        (7, "불국사", "gyeongju", "history", "경북 경주시 불국로",35.7901,129.3321,90,"신라의 역사와 사찰 건축"),
        (8, "동궁과 월지", "gyeongju", "history", "경북 경주시 원화로",35.8346,129.2269,60,"신라 왕궁의 별궁과 연못"),
        (9, "부산박물관", "busan", "museum", "부산 남구 유엔평화로",35.1290,129.0925,60,"실내에서 부산의 역사와 문화를 살펴보는 전시 공간. 운영시간은 시연용입니다."),
        (10, "SEA LIFE 부산아쿠아리움", "busan", "aquarium", "부산 해운대구 해운대해변로",35.1590,129.1608,90,"실내 해양 생물 전시 공간. 운영시간과 입장 가능 여부는 별도 확인이 필요합니다."),
        (11, "울산박물관", "ulsan", "museum", "울산 남구 두왕로",35.5247,129.3086,60,"울산의 역사를 소개하는 실내 전시 공간. 운영시간은 시연용입니다."),
        (12, "장생포 고래박물관", "ulsan", "museum", "울산 남구 장생포고래로",35.5028,129.3809,60,"고래 관련 실내 전시 공간. 운영시간은 시연용입니다."),
        (13, "국립경주박물관", "gyeongju", "museum", "경북 경주시 일정로",35.8297,129.2280,90,"신라 유물을 살펴볼 수 있는 실내 전시 공간. 운영시간은 시연용입니다."),
        (14, "경주솔거미술관", "gyeongju", "gallery", "경북 경주시 경감로",35.8315,129.2828,60,"미술 작품을 감상하는 실내 전시 공간. 운영시간은 시연용입니다."),
    ]
]
CITY_ALIASES = {"부산": "busan", "울산": "ulsan", "경주": "gyeongju"}
PREFERENCE_ALIASES = {"바다": "sea", "카페": "cafe", "역사": "history", "자연": "nature", "사진": "photo", "맛집": "food"}
