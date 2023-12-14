from flask import Flask, jsonify
# from config import Config
# from sanitize import UniversalSanitizerMiddleware
from services.web_views.routes import routes_blueprint
from services.api.users import users_blueprint
import os

from pymongo import MongoClient

client = MongoClient('mongodb+srv://timothee-oliveau:Y6OXjsKKBjKKqAvc@coachingmarketplace.h2hzjxp.mongodb.net/?retryWrites=true&w=majority')
client = MongoClient(os.getenv('PROTOTYPE_DB_CONNECTION_STRING'))

db = client[os.getenv('PROTOTYPE_DB_NAME')]

# mock_coaches = [
#     {
#         "firstName": "Emily",
#         "lastName": "Johnson",
#         "email": "emily.johnson@coachingpro.com",
#         "title": "Life and Career Coach",
#         "tags": ["Personal Development", "Career Growth", "Work-Life Balance"],
#         "hourlyRate": 100,
#         "description": {
#             "hook": "Transform your life and career with personalized guidance!",
#             "experience": "Over 10 years in career counseling and life coaching, certified in NLP and Positive Psychology.",
#             "expertise": ["Career transitions", "personal development", "stress management"],
#             "callToAction": "Ready to take the next step? Book a session directly through my calendar or send me a message to start your journey!"
#         }
#     },
#     {
#         "firstName": "David",
#         "lastName": "Smith",
#         "email": "david.smith@peakperformance.com",
#         "title": "Performance Coach",
#         "tags": ["Peak Performance", "Athletes", "High Achievers"],
#         "hourlyRate": 120,
#         "description": {
#             "hook": "Elevate your performance to world-class levels!",
#             "experience": "15 years coaching professional athletes and high achievers, with a background in sports psychology.",
#             "expertise": ["Elite sports", "mental toughness", "goal setting"],
#             "callToAction": "Want to excel in your field? Schedule a meeting with me or drop a message to begin your transformation!"
#         }
#     },
#     {
#         "firstName": "Angela",
#         "lastName": "Martinez",
#         "email": "angela.m@wellnesscoach.com",
#         "title": "Wellness and Health Coach",
#         "tags": ["Wellness", "Nutrition", "Fitness"],
#         "hourlyRate": 80,
#         "description": {
#             "hook": "Achieve your healthiest self with holistic wellness coaching.",
#             "experience": "8 years as a nutritionist and wellness coach, specializing in holistic health approaches.",
#             "expertise": ["Nutritional planning", "fitness regimes", "stress reduction techniques"],
#             "callToAction": "Ready for a healthier you? Book an appointment on my calendar or send me a message for a personalized wellness plan!"
#         }
#     },
#     {
#         "firstName": "Michael",
#         "lastName": "Lee",
#         "email": "michael.lee@bizcoach.com",
#         "title": "Business Coach",
#         "tags": ["Entrepreneurship", "Business Strategy", "Leadership"],
#         "hourlyRate": 110,
#         "description": {
#             "hook": "Grow your business and leadership skills with expert coaching.",
#             "experience": "12 years of experience in business consultancy and leadership coaching, MBA holder.",
#             "expertise": ["Start-up growth", "leadership development", "strategic planning"],
#             "callToAction": "Want to take your business to the next level? Let's talk! Book a session or message me for tailored business advice."
#         }
#     },
#     {
#         "firstName": "Rachel",
#         "lastName": "Nguyen",
#         "email": "rachel.nguyen@mindfulgrowth.com",
#         "title": "Mindfulness and Stress Management Coach",
#         "tags": ["Mindfulness", "Stress Relief", "Personal Growth"],
#         "hourlyRate": 80,
#         "description": {
#             "hook": "Find peace and productivity through mindfulness.",
#             "experience": "Certified mindfulness practitioner with 5 years of coaching experience.",
#             "expertise": ["Mindfulness techniques", "stress management", "work-life balance"],
#             "callToAction": "Begin your journey to a calmer, more focused life. Book a discovery call or send me a message!"
#         }
#     },
#     {
#         "firstName": "Lucas",
#         "lastName": "Brown",
#         "email": "lucas.brown@executivepath.com",
#         "title": "Executive Leadership Coach",
#         "tags": ["Leadership", "Executive Training", "Corporate Growth"],
#         "hourlyRate": 150,
#         "description": {
#             "hook": "Lead with confidence and vision in the corporate world.",
#             "experience": "Over 20 years in corporate leadership and executive coaching.",
#             "expertise": ["Executive development", "leadership skills", "organizational change"],
#             "callToAction": "Elevate your leadership skills. Schedule a session or reach out for a tailored executive coaching program!"
#         }
#     },
#     {
#         "firstName": "Sara",
#         "lastName": "Patel",
#         "email": "sara.patel@creativecoaching.com",
#         "title": "Creativity and Innovation Coach",
#         "tags": ["Creativity", "Innovation", "Artistic Development"],
#         "hourlyRate": 70,
#         "description": {
#             "hook": "Unleash your creative potential and innovate freely.",
#             "experience": "Creative professional with 7 years of coaching in creative industries.",
#             "expertise": ["Artistic expression", "creative thinking", "innovation strategies"],
#             "callToAction": "Spark your creativity today. Book a meeting or message me for a personalized coaching session!"
#         }
#     },
#     {
#         "firstName": "James",
#         "lastName": "O'Connell",
#         "email": "james.oconnell@financecoach.com",
#         "title": "Financial Wellness Coach",
#         "tags": ["Financial Planning", "Wealth Management", "Retirement Planning"],
#         "hourlyRate": 100,
#         "description": {
#             "hook": "Secure your financial future with expert guidance.",
#             "experience": "Certified Financial Planner with 12 years of experience in financial advising.",
#             "expertise": ["Personal finance", "investment strategies", "retirement planning"],
#             "callToAction": "Ready to achieve financial wellness? Let's talk. Schedule a session or send me a message for financial planning advice."
#         }
#     },
#     {
#         "firstName": "Isabella",
#         "lastName": "Schmidt",
#         "email": "isabella.schmidt@lifetransitions.com",
#         "title": "Transition and Change Coach",
#         "tags": ["Life Transitions", "Personal Change", "Resilience Building"],
#         "hourlyRate": 90,
#         "description": {
#             "hook": "Navigate life's transitions with confidence and clarity.",
#             "experience": "10 years as a coach specializing in major life changes and resilience.",
#             "expertise": ["Career changes", "personal development", "coping strategies"],
#             "callToAction": "Embrace change positively. Book a discovery call or send me a message to start your transformation journey!"
#         }
#     }
# ]

# db['users'].delete_many({})
# db['users'].insert_many(mock_coaches)

app = Flask(__name__)



# app.config.from_object(Config)

# # Apply the Universal Sanitizer Middleware
# app.wsgi_app = UniversalSanitizerMiddleware(app.wsgi_app)

# # Import routes and other parts of your application here
# from your_application import routes, models, etc.

app.register_blueprint(users_blueprint, url_prefix='/api')

app.register_blueprint(routes_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
