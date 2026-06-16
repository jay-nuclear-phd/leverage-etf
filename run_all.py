import os
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
from unittest.mock import patch
import logging

# matplotlib 경고 메시지 숨기기 (폰트 관련 등)
logging.getLogger('matplotlib').setLevel(logging.ERROR)

def run_scripts():
    # 전역 설정
    mpl.rcParams['axes.unicode_minus'] = False

    # 현재 디렉토리의 모든 .py 파일 목록 (자기 자신 제외)
    current_script = os.path.basename(sys.executable if hasattr(sys, 'frozen') else __file__)
    scripts = [f for f in os.listdir('.') if f.endswith('.py') and f != current_script]
    scripts.sort()

    print(f"Found {len(scripts)} scripts to run.")

    # plt.show()를 무시하도록 패치
    with patch('matplotlib.pyplot.show'):
        for script in scripts:
            print(f"--- Running: {script} ---")
            try:
                # 스크립트 실행
                with open(script, 'r', encoding='utf-8') as f:
                    code = f.read()
                    # exec를 사용하여 현재 프로세스 내에서 실행 (plt 패치가 적용됨)
                    # 별도의 globals를 제공하여 스크립트 간 네임스페이스 오염 방지
                    script_globals = {'__name__': '__main__', '__file__': script}
                    exec(code, script_globals)
                print(f"Finished: {script}\n")
            except FileNotFoundError as e:
                print(f"Error running {script}: 데이터 파일이 없습니다. ({e.filename})\n")
            except Exception as e:
                print(f"Error running {script}: {e}\n")

if __name__ == "__main__":
    # plots 폴더 생성 확인
    os.makedirs('plots', exist_ok=True)
    run_scripts()
    print("All simulations completed. Check the 'plots/' folder for results.")
