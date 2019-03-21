from bbq import app, temp_thread

if __name__ == '__main__':
    temp_thread.start()
    app.run(host='0.0.0.0', port=8085)
