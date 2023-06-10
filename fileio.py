import Cmodule  # C 모듈을 import

def save_to_file(inputstr):
    content = str(inputstr)
    filename = 'output.txt'
    
    with open(filename, 'w') as file:
        file.write(content)
    
    print(f"내용이 '{filename}' 파일로 저장되었습니다.")

    # C 모듈의 파일 입출력 함수 호출
    Cmodule.pFileOut(filename, content)
