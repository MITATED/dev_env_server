from app import app
import view
from func import manually

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001, debug=manually)
