import os
import sys

# Add project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wealthbridge.settings')
django.setup()

from django.db import connection

queries = [
    """CREATE TABLE IF NOT EXISTS "bank_app_cryptocurrency" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
        "code" varchar(10) NOT NULL UNIQUE, 
        "name" varchar(50) NOT NULL, 
        "icon" varchar(50) NOT NULL, 
        "min_deposit" decimal NOT NULL, 
        "confirmations_required" integer NOT NULL, 
        "is_active" bool NOT NULL, 
        "sort_order" integer NOT NULL
    );""",
    
    """CREATE TABLE IF NOT EXISTS "bank_app_investmentplan" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
        "name" varchar(100) NOT NULL, 
        "plan_type" varchar(20) NOT NULL, 
        "min_amount" decimal NOT NULL, 
        "max_amount" decimal NOT NULL, 
        "interest_rate" decimal NOT NULL, 
        "duration_days" integer NOT NULL, 
        "description" text NOT NULL, 
        "is_active" bool NOT NULL, 
        "created_at" datetime NOT NULL
    );""",
    
    """CREATE TABLE IF NOT EXISTS "bank_app_systemcryptosetting" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
        "auto_approve_deposits" bool NOT NULL, 
        "deposit_fee_percentage" decimal NOT NULL, 
        "min_deposit_amount" decimal NOT NULL, 
        "max_deposit_amount" decimal NOT NULL, 
        "updated_at" datetime NOT NULL, 
        "updated_by" varchar(150) NULL
    );""",
    
    """CREATE TABLE IF NOT EXISTS "bank_app_userinvestment" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
        "amount_invested" decimal NOT NULL, 
        "expected_return" decimal NOT NULL, 
        "start_date" datetime NOT NULL, 
        "end_date" datetime NOT NULL, 
        "status" varchar(20) NOT NULL, 
        "created_at" datetime NOT NULL, 
        "investment_plan_id" bigint NOT NULL REFERENCES "bank_app_investmentplan" ("id") DEFERRABLE INITIALLY DEFERRED, 
        "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
    );""",
    
    """CREATE TABLE IF NOT EXISTS "bank_app_investmenttransaction" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
        "amount" decimal NOT NULL, 
        "transaction_type" varchar(20) NOT NULL, 
        "description" text NOT NULL, 
        "created_at" datetime NOT NULL, 
        "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, 
        "investment_id" bigint NULL REFERENCES "bank_app_userinvestment" ("id") DEFERRABLE INITIALLY DEFERRED
    );""",
    
    """CREATE TABLE IF NOT EXISTS "bank_app_cryptowalletaddress" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
        "address" varchar(500) NOT NULL, 
        "network" varchar(20) NULL, 
        "is_primary" bool NOT NULL, 
        "is_active" bool NOT NULL, 
        "notes" text NULL, 
        "created_at" datetime NOT NULL, 
        "updated_at" datetime NOT NULL, 
        "created_by" varchar(150) NULL, 
        "crypto_id" bigint NOT NULL REFERENCES "bank_app_cryptocurrency" ("id") DEFERRABLE INITIALLY DEFERRED
    );""",
    
    """CREATE INDEX IF NOT EXISTS "bank_app_userinvestment_investment_plan_id_756c3079" ON "bank_app_userinvestment" ("investment_plan_id");""",
    """CREATE INDEX IF NOT EXISTS "bank_app_userinvestment_user_id_8dc96b97" ON "bank_app_userinvestment" ("user_id");""",
    """CREATE INDEX IF NOT EXISTS "bank_app_investmenttransaction_user_id_b80d6bec" ON "bank_app_investmenttransaction" ("user_id");""",
    """CREATE INDEX IF NOT EXISTS "bank_app_investmenttransaction_investment_id_32347714" ON "bank_app_investmenttransaction" ("investment_id");""",
    """CREATE UNIQUE INDEX IF NOT EXISTS "bank_app_cryptowalletaddress_crypto_id_address_10e9812b_uniq" ON "bank_app_cryptowalletaddress" ("crypto_id", "address");""",
    """CREATE INDEX IF NOT EXISTS "bank_app_cryptowalletaddress_crypto_id_41662b0c" ON "bank_app_cryptowalletaddress" ("crypto_id");"""
]

with connection.cursor() as cursor:
    for query in queries:
        try:
            cursor.execute(query)
        except Exception as e:
            print(f"Error executing: {query[:50]}... -> {e}")

print("Missing tables creation check finished!")
