from parser_class import Parser_class


parser = Parser_class()

if __name__ == "__main__":
    parser.start(int(input("Введите 1 для сбора данных или 0 для просмотра: ")))
