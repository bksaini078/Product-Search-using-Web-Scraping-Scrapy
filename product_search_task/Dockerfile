FROM python:3.9

# We copy just the requirements.txt first to leverage Docker cache

COPY ./product_search /product_search_task/product_search

WORKDIR ./product_search_task/

RUN pip install -r product_search/requirements.txt

EXPOSE 5432
ENTRYPOINT [ "python3","product_search/main.py" ]
