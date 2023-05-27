import requests
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import font

url = 'http://www.sky-map.org/?object=vega'

# # URL에서 XML 데이터 가져오기
# response = requests.get(url)
# xml_string = response.text

# # XML 파싱
# root = ET.fromstring(xml_string)

# # request 요소 찾기
# request_element = root.find('request')

# # 값 설정
# star = input()
# request_element.text = star

# # 수정된 XML 출력
# modified_xml = ET.tostring(root, encoding='utf-8')
# print(modified_xml.decode('utf-8'))