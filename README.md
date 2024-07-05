# delivery_data_crawling

Emart_address.py => 입력한 postcodes에 존재하는 배송 지역의 address_list를 저장하는 코드. 
예를 들어, postcode = "대전광역시 유성구 월평동"일 경우, 해당 지역을 검색했을 때 나오는 모든 주소의 리스트를 저장해서 "addresses_[postcode].csv"로 출력한다.

Emart_search.py => 저장된 지명 주소 리스트를 불러와서 각 주소가 배달 가능한 주소인지 배달 가능 여부를 저장하여 "emart_delivery_status.csv" 파일로 출력한다. 
