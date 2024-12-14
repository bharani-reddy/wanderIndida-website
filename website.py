#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template_string, request, redirect, flash,jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Bharani22003',
    'database': 'reviews'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# State Data with Descriptions
states_data = {
    "Tamil Nadu": {
        "description": "Chennai, the capital city of Tamil Nadu, is a dynamic blend of traditional and contemporary culture. It is a major cultural, economic, and educational center in South India. The city is home to the historic Marina Beach, the vibrant Kapaleeshwarar Temple, and the colonial-era Fort St. George. Chennai's rich cultural heritage, bustling markets, and modern urban lifestyle make it a must-visit destination.",
        "foods": [
            {"name": "Idli and Sambar", "image": "https://www.cookwithmanali.com/wp-content/uploads/2020/05/Masala-Dosa.jpg", "description": "Idli is a soft, fluffy steamed rice cake that is a staple breakfast in South India. It is usually served with sambar, a lentil-based vegetable stew spiced with tamarind. The combination is light yet filling, and is often accompanied by coconut chutney."},
            {"name": "Dosa", "image": "https://www.cookwithmanali.com/wp-content/uploads/2020/05/Masala-Dosa.jpg", "description": "Dosa is a thin, crispy pancake made from a fermented batter of rice and urad dal (black gram). It can be plain or filled with spiced mashed potatoes, known as masala dosa. The dish is typically served with sambar and various chutneys."},
            {"name": "Filter Coffee", "image": "https://www.cookwithmanali.com/wp-content/uploads/2022/03/South-Indian-Filter-Coffee-676x1024.jpg", "description": "Chennai's filter coffee is renowned for its rich aroma and strong flavor. Made using a metal coffee filter, it involves brewing dark roasted coffee beans and chicory. The decoction is mixed with hot milk and sugar, served in a unique stainless steel tumbler and davara."}
],
        "places": [
            {"name": "Ooty", "image": "https://www.tamilnadutourism.tn.gov.in/img/pages/large-desktop/avalanche-hills-ooty-1656333416_e2680b8680086972e69d.webp", "description": "Ooty, also known as Udhagamandalam, is a scenic hill station in the Nilgiri Hills. Known for its cool climate, lush green landscapes, and tea plantations, Ooty is a popular tourist destination. Key attractions include the Ooty Lake, Botanical Gardens, and the Nilgiri Mountain Railway, a UNESCO World Heritage Site."},
            {"name": "Mahabalipuram", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcToO4s8exLKPLYTf2lZjWFmDyL9dCtAxAGwBA&s", "description": "Mahabalipuram, a coastal town, is famous for its ancient rock-cut temples and sculptures. The town, a UNESCO World Heritage Site, features monuments like the Shore Temple, Arjuna's Penance, and the Pancha Rathas. These structures, dating back to the Pallava dynasty, showcase intricate carvings and architectural brilliance."},
            {"name": "Madurai", "image": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/11/71/bf/0e/madurai-meenakshi-temple.jpg?w=1000&h=1000&s=1", "description": "Madurai, known as the City of Temples, is one of the oldest continuously inhabited cities in the world. The city's most famous landmark is the Meenakshi Amman Temple, a magnificent temple complex with intricate sculptures. Madurai is also known for its vibrant bazaars and rich cultural traditions."}
        ]
    },
    "Rajasthan": {
        "description": "Rajasthan, known as the 'Land of Kings', is famous for its deserts, palaces, and vibrant culture.",
        "foods": [
            {"name": "Dal Baati Churma", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6gMaYPBHpyjIDiJmJGK3ZrRmwbck83mMzjg&s", "description": "A traditional Rajasthani dish consisting of baked wheat balls (baati), served with a spicy lentil curry (dal) and a sweet mix of crushed baati, sugar, and ghee (churma). The combination of flavors and textures makes it a unique culinary experience."},
            {"name": "Gatte ki Sabzi", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTd-9lDDPHdtTl4cfhwzgtj_bayBqMJSRuPZw&s", "description": "A spicy curry made with gram flour dumplings cooked in a yogurt-based gravy. The dish is known for its tangy and spicy flavors, often enjoyed with rice or chapati."},
            {"name": "Laal Maas", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSo6GOxzbh2juMYTdDIjdjz6e8wXKUcvhSFyw&s", "description": "A fiery Rajasthani mutton curry made with red chilies and yogurt. The dish is known for its rich, spicy flavor and is a must-try for meat lovers."} 
        ],
        "places": [
            {"name": "Udaipur", "image": "https://static.toiimg.com/thumb/msid-82304823,width-748,height-499,resizemode=4,imgsize-647878/.jpg", "description": "Udaipur, often referred to as the City of Lakes, is known for its picturesque lakes, palaces, and rich cultural heritage. The city is famous for its stunning architecture, including the City Palace, Jag Mandir, and Lake Pichola. Udaipur's romantic setting, combined with its vibrant arts and crafts, makes it a popular destination for tourists."},
            {"name": "Jaipur", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtn194wcPgcbLeZo_CK1B64p-mkKmtlu0P3Q&s", "description": "Jaipur, the capital city of Rajasthan, is known as the Pink City due to the distinct color of its buildings. The city is famous for its majestic forts and palaces, including the Amer Fort, City Palace, and Hawa Mahal. Jaipur's vibrant markets, traditional handicrafts, and rich cultural heritage make it a must-visit destination."},
            {"name": "Neemrana", "image": "https://res.cloudinary.com/simplotel/image/upload/q_80,fl_progressive,w_1500,f_auto,c_fit/neemrana-fort-palace---15th-century-delhi-jaipur-highway/Facade_Premises__Neemrana_Fort_Palace__palace_hotel_in_Rajasthan_14_4_d55b91", "description": "Neemrana is a historical town known for its majestic Neemrana Fort Palace, which has been converted into a luxury heritage hotel. The fort offers stunning views and an immersive experience of Rajasthan's royal heritage. It's a popular destination for weekend getaways and cultural experiences."} 
        ]
    },
    # Add more states here with similar structure...
        "Andhra Pradesh": {
        "description": "Andhra Pradesh is a state in the southern coastal region of India. It is the seventh-largest state and the tenth-most populous in the country. Telugu, one of India's classical languages, is the primary official language and the most widely spoken language in state and as well as in South India.",
        "foods": [
            {"name": "Vada", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRN7HNqDJTF4IBdrD7kDHZJF7miYczRmCiOHA&s", "description": "A savory doughnut-shaped snack made from urad dal, crispy on the outside and soft on the inside, often served with chutney and sambar."},
            {"name": "Chakara Pongal", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhAhMIKy4EhXz7_D-h9VRBBG5Iy3MlY-zrVA&s", "description": "A sweet rice dish made with jaggery, rice, lentils, and ghee, often garnished with cashews and raisins."},
            {"name": "Sambar Rice", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeI-uWSl00MipvIbE9vLof-GfyC6m0TnHo1g&s", "description": "A comforting dish of rice mixed with sambar, a lentil-based vegetable stew. It's a staple food in South India."} 
        ],
        "places": [
            {"name": "Tirumala Temple (Chittoor)", "image": "https://static.toiimg.com/thumb/msid-97189691,imgsize-1694330,width-400,resizemode-4/97189691.jpg", "description": "The Tirumala Temple, dedicated to Lord Venkateswara, is one of the most visited pilgrimage sites in the world. Located on the Tirumala hills near Chittoor, it is renowned for its Dravidian architecture and spiritual significance. Devotees from around the world visit this temple to seek blessings and participate in rituals."},
            {"name": "Sri Mallikarjuna Swamy Temple (Nallamalai Hills)", "image": "https://static.toiimg.com/photo/46918850.cms", "description": "Sri Mallikarjuna Swamy Temple, located in Srisailam, is one of the twelve Jyotirlinga temples dedicated to Lord Shiva. Nestled in the Nallamala Hills, the temple is not only a spiritual destination but also offers scenic views of the surrounding forests and rivers."},
            {"name": "Borra Caves (Ananthagiri Hills, Araku Valley)", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8Dh5Ngtd-wxFEFEBDTkygFO03eqAJtMXJMQ&s", "description": "The Borra Caves, located in the Ananthagiri Hills of the Araku Valley, are famous for their stunning stalactites and stalagmites. The limestone caves, formed over millions of years, are a natural wonder and a popular tourist attraction. The surrounding region is known for its scenic beauty and tribal culture."} 
        ]
    },
        "Karnataka": {
        "description": "Karnataka is a state in southwest India with Arabian Sea coastlines. The capital, Bengaluru (formerly Bangalore), is a high-tech hub known for its shopping and nightlife. To the southwest, Mysore is home to lavish temples including Mysore Palace, former seat of the region’s maharajas. Hampi, once the medieval Vijayanagara empire’s capital, contains ruins of Hindu temples, elephant stables and a stone chariot.",
        "foods": [
            {"name": "Akki Roti", "image": "https://www.masalakorb.com/wp-content/uploads/2020/09/Masala-Akki-Roti-V4.jpg", "description": ": A rice flour flatbread often served with a variety of chutneys and curries."},
            {"name": "Noolputtu", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRcrT4E4PlAQIwNVpqLrve2tGoTdBSqKrZtw&s", "description": "A traditional dish made from rice flour, resembling string hoppers, usually served with coconut milk or spicy curries"},
            {"name": "Kayi Holige", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8YlFs_nsv0ihlHhN9SoaPYkQy87KGOKY5ng&s", "description": "A traditional sweet made from coconut and jaggery stuffed inside a dough made of flour, similar to a sweet flatbread."} 
        ],
        "places": [
            {"name": "Coorg", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlE1Fzwes7IJ-X2LahgGBQE6UysC8--cdI1Q&s", "description": "Coorg, also known as Kodagu, is a scenic hill station in Karnataka renowned for its coffee plantations, lush greenery, and pleasant weather. It's a popular destination for nature lovers and adventure enthusiasts, offering activities like trekking, coffee estate tours, and river rafting."},
            {"name": "Chikmagalur", "image": "https://www.chikmagalurtour.com/images/history-of-chikmagalur.jpg", "description": "Chikmagalur is another beautiful hill station in Karnataka, famous for its coffee plantations, serene landscapes, and trekking spots. It's known for attractions like Mullayanagiri Peak, Baba Budangiri, and the Bhadra Wildlife Sanctuary."},
            {"name": "Nandi Hills", "image": "https://lh7-us.googleusercontent.com/docsz/AD_4nXcMPLLFAr-orS0Y3TwIXDuslCUt7K_Izn5BwQY-6RIIk_pfkMjqjqrEv3B3hfcZhxdlFvq4wHEyaoObPq88_bkBH_LDXYfXGDnBviqpvHCrVjlYwOCgFk5a5q9WfJ8zIBFeKWYieo5c-Sjoye_h7CC6DMgq?key=autnmbA0cWBQre6NkjmCiQ", "description": "Nandi Hills, located near Bangalore, is a popular destination for trekking, paragliding, and experiencing stunning sunrises. The hill station offers a cool climate and picturesque views, making it a favorite weekend getaway."} 
        ]
    },
        "Maharashtra": {
        "description": "Maharashtra is a state in the western peninsular region of India occupying a substantial portion of the Deccan Plateau",
        "foods": [
            {"name": "Pav Bhaji", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgaCo8MyoCR2OLwt9h1CJV5gfSmJX2XEV55w&s", "description": "A spicy vegetable mash served with buttered bread rolls, garnished with onions and lemon."},
            {"name": "Bombay Sandwich", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHDdAzb1Rm9d6P4sV2Hn65N7rpcwIoGsL6jA&s", "description": "A street food sandwich filled with vegetables, chutneys, and sometimes cheese, toasted to perfection."},
            {"name": "Bhel Puri", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsT7NOJ0u1Uqo95XyqIpQLexnsSPODfcyLMw&s", "description": "A popular street snack made from puffed rice, vegetables, and tamarind chutney, offering a mix of sweet, sour, and spicy flavors."} 
        ],
        "places": [
            {"name": "Mumbai", "image": "https://cdn.britannica.com/26/84526-050-45452C37/Gateway-monument-India-entrance-Mumbai-Harbour-coast.jpg", "description": "Mumbai, the capital city of Maharashtra, is a bustling metropolis known for its vibrant culture, historical landmarks, and diverse culinary scene. The city offers a mix of street food and fine dining experiences."},
            {"name": "Pune", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxzgJNrh6Nl3STYCsUNDsSbQRTjkJFcPnHvQ&s", "description": "Pune is a cultural and educational hub in Maharashtra, known for its historical sites, vibrant arts scene, and pleasant weather. The city's culinary scene is a blend of traditional Maharashtrian cuisine and contemporary dishes."},
            {"name": "Gateway of India", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWKCIzwvkxuY07GACaCjctEolpsTUMJQ-H0w&s", "description": "The Gateway of India is an iconic monument in Mumbai, overlooking the Arabian Sea. Built in the Indo-Saracenic style, it commemorates the visit of King George V and Queen Mary to India in 1911. It's a popular spot for tourists and a starting point for exploring Mumbai."} 
        ]
    },
    
}


# HTML Template
html_template = '''

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WonderIndia - Explore India's Diverse Culture</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #333 ;
            margin: 0;
            padding: 0;
            color: #333;
        }

        .header {
            background: linear-gradient(135deg, #1d1d1d, #3e3e3e);
            color: white;
            text-align: center;
            padding: 40px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }

.header h1 {
    font-size: 36px;
    margin: 0;
}

.state-list {
    display: flex;
    justify-content: space-evenly;
    flex-wrap: wrap;
    margin-top: 40px;
    padding: 20px;
}

.state-item {
    margin: 20px;
    padding: 15px;
    background: #fff;
    border: 1px solid #e4e4e4;
    border-radius: 12px;
    text-align: center;
    cursor: pointer;
    width: 220px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.state-item:hover {
    background: #f7f7f7;
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.state-item img {
    width: 100%;
    border-radius: 8px;
    margin-bottom: 15px;
}

.state-item h3 {
    font-size: 22px;
    color: #333;
    margin: 0;
}

.content {
    padding: 50px;
    max-width: 1200px;
    margin: 0 auto;
}

/* Centering the main state title */
.state-name {
    color: white;
    font-size: 2.5em; /* Slightly larger for the main state title */
    font-weight: bold;
    text-align: center;
    background-color: #333;
    padding: 10px;
    border-radius: 5px;
    margin: 20px auto; /* Center the state title */
    width: auto;
    display: block;
}

/* Centering the Famous Foods and Famous Places titles */
.food h2, .place h3 {
    color: white;
    font-size: 2em;
    font-weight: bold;
    text-align: center;
    background-color: #333;
    padding: 10px;
    border-radius: 5px;
    width: auto; /* Ensure it's not taking up more width than necessary */
    margin: 20px auto; /* Centered horizontally with some spacing */
    display: block;
}

.description {
    background: #ffffff;
    border-radius: 8px;
    padding: 25px;
    margin-bottom: 40px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.description h2 {
    font-size: 28px;
    color: #ffdead;
    margin-bottom: 15px;
}

.description p {
    font-size: 18px;
    line-height: 1.6;
}

.food, .place {
    display: flex;
    justify-content: space-evenly; ;
    flex-wrap: wrap;
    text-align: center;
    align-items: center;
    margin-top: 30px;
}

.food div, .place div {
    margin: 15px;
    text-align: center;
    width: 220px;
    background-color: #f4f4f4;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}


.food div:hover, .place div:hover {
    background-color: #f1f1f1;
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.food img, .place img {
    width: 100%;
    border-radius: 10px;
    margin-bottom: 15px;
}
    .food b, .place b {
        display: block;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #f9f9f9;
        margin-bottom: 10px;
        font-weight: bold;
        text-align: center;
    }

        .reviews {
            margin-top: 50px;
            padding: 30px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            position: relative;
        }

        .review-item {
            display: none;
            text-align: center;
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 5px solid #ff9800;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
        }
.review-item p {
    margin: 5px 0;
    font-size: 16px;
}

.review-item small {
    font-size: 14px;
    color: #777;
}

        .add-review {
            background: #fff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            margin-top: 40px;
        }

        .add-review h3 {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
        }
                .add-review form {
            display: grid;
            gap: 15px;
        }

.add-review form input, .add-review form textarea {
    width: 100%;
    padding: 12px;
    margin-bottom: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
    box-sizing: border-box;
    transition: border-color 0.3s ease;
}

.add-review form input:focus, .add-review form textarea:focus {
    border-color: #ff9800;
    outline: none;
}

        .add-review form button {
            padding: 12px;
            background-color: #ff9800;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .add-review form button:hover {
            background-color: #f57c00;
        }
        .review-item.active {
            display: block;
        }
        .add-review form select,
        .add-review form input {
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        .add-review form select:focus,
        .add-review form input:focus {
            border-color: #ff9800;
            outline: none;
        }

    </style>
</head>
<body>
    <div class="header">
        <h1>WonderIndia - Explore India's Diverse Culture</h1>
        <p>Click on a state to explore famous foods, places, and more!</p>
    </div>
    <div class="state-list">
        {% for state, data in states.items() %}
        <div class="state-item" onclick="window.location.href='{{ state }}'">
            <h3>{{ state }}</h3>
        </div>
        {% endfor %}
    </div>

    {% if state_data %}
    <div class="content">
        <h2 class="state-name">{{ state_name }}</h2>
        <div class="description">
            <p>{{ state_data['description'] }}</p>
        </div>

        <div class="food">
            <h2>Famous Foods</h2>
            {% for food in state_data['foods'] %}
            <div>
                <img src="{{ food.image }}" alt="{{ food.name }}">
                <b><p>{{ food.name }}</p></b>
                <b><p>{{ food.description }}</p></b>
            </div>
            {% endfor %}
        </div>

        <div class="place">
            <h3>Famous Places</h3>
            {% for place in state_data['places'] %}
            <div>
                <img src="{{ place.image }}" alt="{{ place.name }}">
                <b><p>{{ place.name }}</p></b>
                <b><p>{{ place.description }}</p></b>
            </div>
            {% endfor %}
        </div>

<!-- Reviews Section -->
    <div class="reviews">
        <h3>User Reviews</h3>
        {% if reviews %}
            {% for review in reviews %}
            <div class="review-item">
                <strong>{{ review['reviewer_name'] }}</strong> reviewed <b>{{ review['place_name'] }}</b>:
                <p>{{ review['review'] }}</p>
                <small>{{ review['created_at'] }}</small>
            </div>
            {% endfor %}
        {% else %}
            <p>No reviews yet. Be the first to add one!</p>
        {% endif %}
    </div>

    <!-- Add Review Form -->
    <div class="add-review">
        <h3>Submit Your Review</h3>
        <form id="review-form">
            <select name="state_name" id="state-dropdown" required>
                <option value="" disabled selected>Select a state</option>
                <option value="Tamil Nadu">Tamil Nadu</option>
                <option value="Rajasthan">Rajasthan</option>
                <option value="Andhra Pradesh">Andhra Pradesh</option>
                <option value="Karnataka">Karnataka</option>
                <option value="Maharashtra">Maharashtra</option>
            </select>

            <select name="place_name" id="place-dropdown" required>
                <option value="" disabled selected>Select a place</option>
            </select>

            <select name="review" id="review" required>
                <option value="" disabled selected>Rate your experience</option>
                <option value="Excellent">Excellent</option>
                <option value="Good">Good</option>
                <option value="Average">Average</option>
                <option value="Poor">Poor</option>
                <option value="Terrible">Terrible</option>
            </select>

            <input type="text" id="reviewer_name" name="reviewer_name" placeholder="Enter your name" required>

            <button type="button" id="submit-btn">Submit</button>
        </form>





</div>


<script>
 let currentReviewIndex = 0;
        const reviews = document.querySelectorAll('.review-item');

        function showNextReview() {
            if (reviews.length > 0) {
                reviews.forEach((review, index) => {
                    review.classList.toggle('active', index === currentReviewIndex);
                });
                currentReviewIndex = (currentReviewIndex + 1) % reviews.length;
            }
        }

        setInterval(showNextReview, 10000);
        showNextReview(); // Show the first review immediately
document.getElementById('state-dropdown').addEventListener('change', function() {
    const state = this.value;
    const places = {
        'Tamil Nadu': ['Ooty', 'Mahabalipuram', 'Madurai'],
        'Rajasthan': ['Udaipur', 'Jaipur', 'Neemrana'],
        'Andhra Pradesh': ['Tirumala Temple (Chittoor)', 'Sri Mallikarjuna Swamy Temple (Nallamalai Hills)', 'Borra Caves (Ananthagiri Hills, Araku Valley)'],
        'Karnataka': ['Coorg', 'Chikmagalur', 'Nandi Hills'],
        'Maharashtra': ['Mumbai', 'Pune', 'Gateway of India']
    };

    const placeDropdown = document.getElementById('place-dropdown');
    placeDropdown.innerHTML = '<option value="" disabled selected>Select a place</option>'; // Reset dropdown

    if (state && places[state]) {
        places[state].forEach(place => {
            const option = document.createElement('option');
            option.value = place;
            option.textContent = place;
            placeDropdown.appendChild(option);
        });
    }
});

document.getElementById('submit-btn').addEventListener('click', function() {
    const stateName = document.getElementById('state-dropdown').value;
    const placeName = document.getElementById('place-dropdown').value;
    const review = document.getElementById('review').value;
    const reviewerName = document.getElementById('reviewer_name').value;

    // Validate inputs
    if (!stateName || !placeName || !review || !reviewerName) {
        alert('Please fill all fields.');
        return;
    }

    // Submit review via AJAX
    fetch('/api/add_review', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            state_name: stateName,
            place_name: placeName,
            review: review,
            reviewer_name: reviewerName,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Review added successfully!');
            location.reload(); // Reload to display the new review
        } else {
            alert('Failed to add review: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

</script>


    </div>
    {% endif %}
</body>
</html>
'''
@app.route('/')
def index():
    return render_template_string(html_template, states=states_data)

@app.route('/<state_name>')
def state_details(state_name):
    # Fetch state data
    state_data = states_data.get(state_name)
    
    # Fetch reviews for the selected state
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT place_name, review, reviewer_name, created_at FROM reviews WHERE state_name = %s", (state_name,))
    reviews = cursor.fetchall()
    conn.close()

    # Format reviews for template
    formatted_reviews = [
        {
            'place_name': review[0],
            'review': review[1],
            'reviewer_name': review[2],
            'created_at': review[3].strftime('%Y-%m-%d %H:%M:%S')
        }
        for review in reviews
    ]

    # Render the template
    if state_data:
        return render_template_string(
            html_template,
            state_name=state_name,
            state_data=state_data,
            reviews=formatted_reviews,
            states=states_data
        )
    return "State not found", 404


@app.route('/api/add_review', methods=['POST'])
def add_review_api():
    # Retrieve data from the form
    state_name = request.form.get('state_name')
    place_name = request.form.get('place_name')
    review = request.form.get('review')
    reviewer_name = request.form.get('reviewer_name')

    # Debugging: Log received data
    app.logger.debug(f"Received: state_name={state_name}, place_name={place_name}, review={review}, reviewer_name={reviewer_name}")

    # Check if all fields are provided
    if not (state_name and place_name and review and reviewer_name):
        return jsonify({'status': 'error', 'message': 'Missing form fields'}), 400

    # Insert data into the database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reviews (state_name, place_name, review, reviewer_name, created_at) VALUES (%s, %s, %s, %s, NOW())",
            (state_name, place_name, review, reviewer_name)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Review added successfully'})
    except Exception as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({'status': 'error', 'message': 'Database error'}), 500



if __name__ == '__main__':
    app.run(debug=False)


# In[ ]:




