<a id="readme-top"></a>
<br />
<div align="center">
  <a href="[https://github.com/othneildrew/Best-README-Template](https://github.com/smalldjangoking/FishMarket)">
    <img src="https://raw.githubusercontent.com/smalldjangoking/FishMarket/refs/heads/main/FishMarket/static/img/logo-banner.png" alt="Logo" width="120">
  </a>

  <h3 align="center">FishMarket - Online Store</h3>

  <p align="center">
    An awesome online store for buying seafood
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#Screenshots">Screenshots</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
![Product Page](https://i.imgur.com/9ZvY87j.png)

The website features a simple yet elegant design. It is optimized for both mobile phones and desktop devices. Easy to manage and user-friendly.

### Key Features of Functionality

- **Buy Products Without Registration**  
  - Shop effortlessly without the need to create an account—perfect for quick and hassle-free purchases.

- **Authentication System via Email**  
  - No personal data required—just email verification to get started.  
  - After placing the first order, user details are securely saved in a personal account for faster future orders.  
  - Additional benefits include:  
    - **Discount Accumulation**: Earn rewards with every purchase.  
    - **Order History**: Easily track past orders (Check status of all orders).  
    - **Delivery Address History**: Save addresses for convenience (with an option to delete if needed).

- **Product's Viewing Page**  
  - Browse products effortlessly with:  
    - **Sort by Price**: Find items within your budget.  
    - **Search by Product Name**: Quickly locate what you need.  
    - **Sort by Category**: Filter products by type for a tailored experience.

- **Product Detail**  
  - Customize your purchase with:  
    - **Choose by Weight and Quantity**: Select products based on specific weight and amount.  
    - **Choose by Quantity Only**: Available for pre-set items.  
    - **Additional Features**: View multiple product images and detailed descriptions.

- **Shopping Cart**  
  - Review and modify your list of selected products before checkout with full control over your order.

- **Checkout Process**  
  - Flexible delivery options via **Nova Poshta**, including:  
    - **To Warehouse**: Pick up at a nearby location.  
    - **To Parcel Locker**: Convenient self-service pickup.  
    - **Courier Delivery**: Straight to your door.  
  - Delivery data is sourced from the **Nova Poshta API**, ensuring up-to-date information with daily automatic updates.

- **Admin Panel & Telegram Bot for Managers**  
  - Manage orders efficiently with two powerful tools:  
    - **Django Admin Panel**: A fully functional interface for processing and tracking orders.  
    - **Telegram Bot**: A companion tool designed for managers, offering:  
      - **Control Status of Order**: Mark orders as "Paid" and update statuses via a menu with various options.
      - **Track Delivered Orders**: Check all orders with status in ['progress', 'Order Sent']
      - **Search Orders**: Find specific orders by ID or customer email.  
      - **Real-Time Notifications**: Receive instant updates in Telegram whenever a new order is placed, including key order details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This project is powered by the following technologies:

* [![Python][Python]][Python-url]
* [![Django][Django]][Django-url]
* [![HTML5][HTML5]][HTML5-url]
* [![CSS3][CSS3]][CSS3-url]
* [![jQuery][jQuery]][jQuery-url]
* [![JavaScript][JavaScript]][JavaScript-url]
* [![Aiogram][Aiogram]][Aiogram-url]
* [![Celery][Celery]][Celery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Follow the instructions for a quick and easy project setup.

### Prerequisites
* git
* docker/docker-compose

### Installation

_To quickly deploy the project, you’ll launch it using Docker after setting up the required API keys and settings.py file._

1. Get a Novaposhta API Key at [https://api-portal.novapost.com](https://api-portal.novapost.com/uk/api-nova-post/start/api-keys/)
2. Create your own bot in telegram [BotFather](https://t.me/BotFather) and get the API token
3. Clone the repo
   ```sh
   git clone https://github.com/smalldjangoking/FishMarket.git
   ```
4. Update the `.env` file by adding your authorization data and the API keys obtained from steps _1_ and _2_
   ```sh
   DJANGO_SUPERUSER_EMAIL=
   DJANGO_SUPERUSER_PASSWORD=
   ...
   NOVAPOSHTA_API=YOUR_NOVAPOSHTA_API
   TELEGRAM_API=YOUR_TELEGRAM_BOT_API_TOKEN
   TELEGRAM_BOT_ID=YOUR_BOT_TELEGRAM_ID
   ```
5. Update the `settings.py` file with the SMTP configuration for the email client
6. Run the application `cd FishMarket`
   ```sh
   docker-compose up --build
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Screenshots EXAMPLES -->
## Screenshots

Below are some highlights of the FishMarket online store interface and functionality:

| **Feature**          | **Screenshot**                                                                 |
|----------------------|--------------------------------------------------------------------------------|
| **Telegram Bot**     | ![Telegram Bot](https://i.imgur.com/WM8S49b.png)                              |
| **Landing Page**     | ![Landing Page](https://i.imgur.com/kPhxyLM.png)                              |
| **User Profile**     | ![User Profile](https://i.imgur.com/J6Qqrgk.png)                              |
| **Order History**    | ![Order History](https://i.imgur.com/1NNYZwr.png)                             |
| **Product Page**     | ![Product Page](https://i.imgur.com/mjj1IbZ.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->


<!-- Links for Built With -->
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Django]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[HTML5]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white
[HTML5-url]: https://developer.mozilla.org/en-US/docs/Web/HTML
[CSS3]: https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white
[CSS3-url]: https://developer.mozilla.org/en-US/docs/Web/CSS
[jQuery]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[jQuery-url]: https://jquery.com/
[JavaScript]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[Aiogram]: https://img.shields.io/badge/Aiogram-0088CC?style=for-the-badge&logo=telegram&logoColor=white
[Aiogram-url]: https://aiogram.dev/
[Celery]: https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white
[Celery-url]: https://docs.celeryproject.org/
