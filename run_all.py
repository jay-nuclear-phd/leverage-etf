import os
import sys
import matplotlib.pyplot as plt
from unittest.mock import patch

def run_scripts():
    # 현재 디렉토리의 모든 .py 파일 목록 (자기 자신 제외)
    current_script = os.path.basename(__sys_executable__ if hasattr(sys, 'frozen') else __file__)
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
                    exec(code, {'__name__': '__main__', '__file__': script})
                print(f"Finished: {script}\n")
            except Exception as e:
                print(f"Error running {script}: {e}\n")

if __name__ == "__main__":
    # plots 폴더 생성 확인
    os.makedirs('plots', exist_ok=True)
    run_scripts()
    print("All simulations completed. Check the 'plots/' folder for results.")
