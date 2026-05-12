#!/bin/bash
set -e

ENDPOINT_URL="http://localhost:8001"
REGION="eu-west-1"

export AWS_ACCESS_KEY_ID=fake
export AWS_SECRET_ACCESS_KEY=fake
export AWS_DEFAULT_REGION=$REGION

ADMIN_ID="11111111-1111-1111-1111-111111111111"
USER_ID="22222222-2222-2222-2222-222222222222"

CAR_1_ID="33333333-3333-3333-3333-333333333333"
CAR_2_ID="44444444-4444-4444-4444-444444444444"

TRIP_1_ID="55555555-5555-5555-5555-555555555555"
TRIP_2_ID="66666666-6666-6666-6666-666666666666"

COMMIT_1_ID="77777777-7777-7777-7777-777777777777"
COMMIT_2_ID="88888888-8888-8888-8888-888888888888"
COMMIT_3_ID="99999999-9999-9999-9999-999999999999"

REFUELING_1_ID="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
REFUELING_2_ID="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"

ADMIN_EMAIL="admin@test.com"
USER_EMAIL="user@test.com"

ADMIN_HASH='$argon2id$v=19$m=65536,t=3,p=4$r6WdjH6rFR/wl38nBO5Blg$+OJHw767tnYiXqD86x5rCPT5EGDCRUsJgLAzRrU/BjM'
USER_HASH='$argon2id$v=19$m=65536,t=3,p=4$r6WdjH6rFR/wl38nBO5Blg$+OJHw767tnYiXqD86x5rCPT5EGDCRUsJgLAzRrU/BjM'

create_table_if_not_exists() {
  TABLE_NAME=$1
  shift

  if aws dynamodb describe-table \
    --table-name "$TABLE_NAME" \
    --endpoint-url "$ENDPOINT_URL" >/dev/null 2>&1; then
    echo "[SKIP] Table $TABLE_NAME already exists"
  else
    echo "[CREATE] Table $TABLE_NAME"
    aws dynamodb create-table "$@" --endpoint-url "$ENDPOINT_URL"
  fi
}

create_table_if_not_exists users \
  --table-name users \
  --attribute-definitions \
      AttributeName=id,AttributeType=S \
      AttributeName=email,AttributeType=S \
  --key-schema \
      AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --global-secondary-indexes '[
    {
      "IndexName": "email-index",
      "KeySchema": [
        {"AttributeName": "email", "KeyType": "HASH"}
      ],
      "Projection": {"ProjectionType": "ALL"}
    }
  ]'

create_table_if_not_exists cars \
  --table-name cars \
  --attribute-definitions \
      AttributeName=id,AttributeType=S \
      AttributeName=plate,AttributeType=S \
  --key-schema \
      AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --global-secondary-indexes '[
    {
      "IndexName": "plate-index",
      "KeySchema": [
        {"AttributeName": "plate", "KeyType": "HASH"}
      ],
      "Projection": {"ProjectionType": "ALL"}
    }
  ]'

create_table_if_not_exists trips \
  --table-name trips \
  --attribute-definitions \
      AttributeName=id,AttributeType=S \
      AttributeName=user_id,AttributeType=S \
      AttributeName=car_id,AttributeType=S \
      AttributeName=status,AttributeType=S \
  --key-schema \
      AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --global-secondary-indexes '[
    {
      "IndexName": "user_id-index",
      "KeySchema": [
        {"AttributeName": "user_id", "KeyType": "HASH"}
      ],
      "Projection": {"ProjectionType": "ALL"}
    },
    {
      "IndexName": "car_id-index",
      "KeySchema": [
        {"AttributeName": "car_id", "KeyType": "HASH"}
      ],
      "Projection": {"ProjectionType": "ALL"}
    },
    {
      "IndexName": "car_id-status-index",
      "KeySchema": [
        {"AttributeName": "car_id", "KeyType": "HASH"},
        {"AttributeName": "status", "KeyType": "RANGE"}
      ],
      "Projection": {"ProjectionType": "ALL"}
    }
  ]'

create_table_if_not_exists refuelings \
  --table-name refuelings \
  --attribute-definitions \
      AttributeName=id,AttributeType=S \
      AttributeName=car_id,AttributeType=S \
  --key-schema \
      AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --global-secondary-indexes '[
    {
      "IndexName": "car_id-index",
      "KeySchema": [
        {"AttributeName": "car_id", "KeyType": "HASH"}
      ],
      "Projection": {"ProjectionType": "ALL"}
    }
  ]'

create_table_if_not_exists commits \
  --table-name commits \
  --attribute-definitions \
      AttributeName=id,AttributeType=S \
      AttributeName=code,AttributeType=S \
  --key-schema \
      AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --global-secondary-indexes '[
    {
      "IndexName": "code-index",
      "KeySchema": [
        {"AttributeName": "code", "KeyType": "HASH"}
      ],
      "Projection": {"ProjectionType": "ALL"}
    }
  ]'

echo "[UPSERT] Users"

aws dynamodb put-item \
  --table-name users \
  --item "{
    \"id\": {\"S\": \"$ADMIN_ID\"},
    \"name\": {\"S\": \"admin\"},
    \"email\": {\"S\": \"$ADMIN_EMAIL\"},
    \"hashed_password\": {\"S\": \"$ADMIN_HASH\"},
    \"role\": {\"S\": \"ADMIN\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name users \
  --item "{
    \"id\": {\"S\": \"$USER_ID\"},
    \"name\": {\"S\": \"Mario Rossi\"},
    \"email\": {\"S\": \"$USER_EMAIL\"},
    \"hashed_password\": {\"S\": \"$USER_HASH\"},
    \"role\": {\"S\": \"USER\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

echo "[UPSERT] Cars"

aws dynamodb put-item \
  --table-name cars \
  --item "{
    \"id\": {\"S\": \"$CAR_1_ID\"},
    \"plate\": {\"S\": \"AB123CD\"},
    \"model\": {\"S\": \"Fiat Panda\"},
    \"co2_per_km\": {\"N\": \"95.5\"},
    \"status\": {\"S\": \"FREE\"},
    \"mileage\": {
      \"M\": {
        \"km_total\": {\"N\": \"45000\"},
        \"km_servicing\": {\"N\": \"50000\"},
        \"km_wheels\": {\"N\": \"60000\"}
      }
    },
    \"fuel_info\": {
      \"M\": {
        \"type\": {\"S\": \"DIESEL\"},
        \"level\": {\"N\": \"70\"},
        \"card\": {\"S\": \"CARD-001\"}
      }
    }
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name cars \
  --item "{
    \"id\": {\"S\": \"$CAR_2_ID\"},
    \"plate\": {\"S\": \"EF456GH\"},
    \"model\": {\"S\": \"Toyota Yaris\"},
    \"co2_per_km\": {\"N\": \"88.2\"},
    \"status\": {\"S\": \"IN_USE\"},
    \"mileage\": {
      \"M\": {
        \"km_total\": {\"N\": \"23000\"},
        \"km_servicing\": {\"N\": \"30000\"},
        \"km_wheels\": {\"N\": \"40000\"}
      }
    },
    \"fuel_info\": {
      \"M\": {
        \"type\": {\"S\": \"GASOLINE\"},
        \"level\": {\"N\": \"45\"},
        \"card\": {\"S\": \"CARD-002\"}
      }
    }
  }" \
  --endpoint-url "$ENDPOINT_URL"

echo "[UPSERT] Trips"

aws dynamodb put-item \
  --table-name trips \
  --item "{
    \"id\": {\"S\": \"$TRIP_1_ID\"},
    \"car_id\": {\"S\": \"$CAR_1_ID\"},
    \"user_id\": {\"S\": \"$USER_ID\"},
    \"start_position\": {\"S\": \"Roma\"},
    \"end_position\": {\"S\": \"Napoli\"},
    \"start_date\": {\"S\": \"2026-05-10T08:00:00+00:00\"},
    \"end_date\": {\"S\": \"2026-05-10T11:00:00+00:00\"},
    \"start_km\": {\"N\": \"45000\"},
    \"end_km\": {\"N\": \"45225\"},
    \"status\": {\"S\": \"closed\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name trips \
  --item "{
    \"id\": {\"S\": \"$TRIP_2_ID\"},
    \"car_id\": {\"S\": \"$CAR_2_ID\"},
    \"user_id\": {\"S\": \"$USER_ID\"},
    \"start_position\": {\"S\": \"Milano\"},
    \"start_date\": {\"S\": \"2026-05-12T09:00:00+00:00\"},
    \"start_km\": {\"N\": \"23000\"},
    \"status\": {\"S\": \"active\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

echo "[UPSERT] Commits"

aws dynamodb put-item \
  --table-name commits \
  --item "{
    \"id\": {\"S\": \"$COMMIT_1_ID\"},
    \"code\": {\"S\": \"COMM-001\"},
    \"description\": {\"S\": \"Intervento cliente Napoli\"},
    \"status\": {\"S\": \"DONE\"},
    \"trip_id\": {\"S\": \"$TRIP_1_ID\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name commits \
  --item "{
    \"id\": {\"S\": \"$COMMIT_2_ID\"},
    \"code\": {\"S\": \"COMM-002\"},
    \"description\": {\"S\": \"Ritiro materiali Roma\"},
    \"status\": {\"S\": \"DONE\"},
    \"trip_id\": {\"S\": \"$TRIP_1_ID\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name commits \
  --item "{
    \"id\": {\"S\": \"$COMMIT_3_ID\"},
    \"code\": {\"S\": \"COMM-003\"},
    \"description\": {\"S\": \"Trasferta Milano\"},
    \"status\": {\"S\": \"IN_PROGRESS\"},
    \"trip_id\": {\"S\": \"$TRIP_2_ID\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

echo "[UPSERT] Refuelings"

aws dynamodb put-item \
  --table-name refuelings \
  --item "{
    \"id\": {\"S\": \"$REFUELING_1_ID\"},
    \"date\": {\"S\": \"2026-05-10T07:30:00+00:00\"},
    \"car_id\": {\"S\": \"$CAR_1_ID\"},
    \"liter_price\": {\"N\": \"1.82\"},
    \"liters\": {\"N\": \"40.5\"},
    \"receipt_photo\": {\"S\": \"receipts/$REFUELING_1_ID.jpg\"},
    \"card_number\": {\"S\": \"CARD-001\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name refuelings \
  --item "{
    \"id\": {\"S\": \"$REFUELING_2_ID\"},
    \"date\": {\"S\": \"2026-05-12T08:30:00+00:00\"},
    \"car_id\": {\"S\": \"$CAR_2_ID\"},
    \"liter_price\": {\"N\": \"1.76\"},
    \"liters\": {\"N\": \"32.2\"},
    \"receipt_photo\": {\"S\": \"receipts/$REFUELING_2_ID.jpg\"},
    \"card_number\": {\"S\": \"CARD-002\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

echo "[DONE] Local DynamoDB initialized with mock data"