import bbq


def main():
    bbq.temp_thread.start()
    return bbq.app


app = main()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085)
