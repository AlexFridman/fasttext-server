# bot-back


## Getting Started

These instructions will get you up and running with bot-back.

### Prerequisites

* Python 3 (see [here for instructions](http://docs.python-guide.org/en/latest/starting/installation/))
* FastText for Python (see [here for instructions](https://github.com/facebookresearch/fastText#building-fasttext-for-python))


### Up&Run

```bash
docker build -t bot-back .
docker run -v /tmp/models:/app/models -p 8000:8000 -t bot-back /app/models
```