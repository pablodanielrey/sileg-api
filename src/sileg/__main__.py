
from sileg import app

def main():
    app.run(host='0.0.0.0', port=10203, debug=False)

if __name__ == '__main__':
    main()