import traceback
import sys

if '-t' in sys.argv and __name__ == '__main__':
    # Тестовый режим запуска
    try:
        from app import test
        test()
    except Exception as ex:
        print(ex)
        print(traceback.format_exc())
elif __name__ == '__main__':
    # Релизный режим запуска
    try:
        from app import main
        main()
    except Exception as ex:
        print(ex)
        print(traceback.format_exc())