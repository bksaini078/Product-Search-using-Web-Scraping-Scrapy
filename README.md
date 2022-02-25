# Product-Search-using-Web-Scraping-Scrapy
Search for specific product details from website using scrapy.

Important folders and files details to run the the code.


    Product_Search
        Configurations--> Contains configuration detials for the experiment and modify/add as per requirements.
        product_details.xlsx --> contain product details, add the brand and product name here.
        config.json-->  Define rules, selectors, and product details, you want to search. Add/Modify accordingly.

    Database--> Contains the database and output file. 
                Note: For now, code delete the existing database and create new at every run of the task.

    Spiders--> Contains scraping code.
        run_scripts.sh--> shell script to run scrap_product.py
        scrap_product.py--> scraping and adding in database code.

    main.py--> Main program to run the complete task.
                Note: The web app can run parallely, the purpose of running the task at once was my intention.

    Requirements.txt--> requirements related to task



Reference: 
Docker image available
```
bksaini078/product_search_scrap:latest
docker run -it -p 5432:5432 bksaini078/product_search_scrap:latest
```
