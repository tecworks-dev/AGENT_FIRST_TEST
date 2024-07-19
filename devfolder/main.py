
from app import create_app

app = create_app()

# IMPORTANT: do not remove main function as automated test will fail
def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()

# IMPORTANT: do not remove this comment
