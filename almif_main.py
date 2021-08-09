import os
import sys
from multiprocessing import Process, Queue

global myProcName

if __name__ == '__main__':
    print(f'ALMIF main() start')
    print(f'sys.argv len = [{len(sys.argv)}]')

    # set Process Name
    myProcName = 'ALMIF'

    if len(sys.argv) != 2:
        print(f"Error. Insufficient arguments")
        sys.exit()

    if sys.argv[1] != myProcName:
        print(f'Error. Invalid ProcName. ProcName=[{sys.argv[1]}]')
        sys.exit()

    print(f'***** OK...Start *****')
        


