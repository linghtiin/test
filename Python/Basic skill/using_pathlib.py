from pathlib import Path

main_path = Path('.')

index_html = main_path.glob('*.py')
for i in index_html:
    print(i)

for i in main_path.iterdir():
    print(i)


with (main_path/'t1.proto').open() as fp:
    for i in fp.readlines():
        print(i)
        