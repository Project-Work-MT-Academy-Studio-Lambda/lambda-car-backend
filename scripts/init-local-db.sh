#!/bin/sh
set -e

ENDPOINT_URL="${ENDPOINT_URL:-http://localhost:8001}"
REGION="${AWS_DEFAULT_REGION:-eu-west-1}"

export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-fake}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-fakepassword}"
export AWS_DEFAULT_REGION=$REGION

ADMIN_ID="11111111-1111-1111-1111-111111111111"
USER_ID="22222222-2222-2222-2222-222222222222"
USER_2_ID="22222222-2222-2222-2222-222222222223"
USER_3_ID="22222222-2222-2222-2222-222222222224"

CAR_1_ID="33333333-3333-3333-3333-333333333333"
CAR_2_ID="44444444-4444-4444-4444-444444444444"
CAR_3_ID="33333333-3333-3333-3333-333333333334"
CAR_4_ID="33333333-3333-3333-3333-333333333335"
CAR_5_ID="33333333-3333-3333-3333-333333333336"

TRIP_1_ID="55555555-5555-5555-5555-555555555555"
TRIP_2_ID="66666666-6666-6666-6666-666666666666"
TRIP_3_ID="55555555-5555-5555-5555-555555555556"
TRIP_4_ID="55555555-5555-5555-5555-555555555557"
TRIP_5_ID="55555555-5555-5555-5555-555555555558"

COMMIT_1_ID="77777777-7777-7777-7777-777777777777"
COMMIT_2_ID="88888888-8888-8888-8888-888888888888"
COMMIT_3_ID="99999999-9999-9999-9999-999999999999"
COMMIT_4_ID="77777777-7777-7777-7777-777777777778"
COMMIT_5_ID="77777777-7777-7777-7777-777777777779"
COMMIT_6_ID="77777777-7777-7777-7777-777777777780"
COMMIT_7_ID="77777777-7777-7777-7777-777777777781"

REFUELING_1_ID="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
REFUELING_2_ID="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
REFUELING_3_ID="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaab"
REFUELING_4_ID="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaac"
REFUELING_5_ID="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaad"

MAINTENANCE_1_ID="dddddddd-dddd-dddd-dddd-dddddddddddd"
MAINTENANCE_2_ID="eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"
MAINTENANCE_3_ID="ffffffff-ffff-ffff-ffff-ffffffffffff"
MAINTENANCE_4_ID="dddddddd-dddd-dddd-dddd-ddddddddddde"
MAINTENANCE_5_ID="dddddddd-dddd-dddd-dddd-dddddddddddf"

ADMIN_EMAIL="admin@test.com"
USER_EMAIL="user@test.com"
USER_2_EMAIL="giulia.bianchi@test.com"
USER_3_EMAIL="luca.verdi@test.com"

ADMIN_HASH='$argon2id$v=19$m=65536,t=3,p=4$r6WdjH6rFR/wl38nBO5Blg$+OJHw767tnYiXqD86x5rCPT5EGDCRUsJgLAzRrU/BjM'
USER_HASH='$argon2id$v=19$m=65536,t=3,p=4$r6WdjH6rFR/wl38nBO5Blg$+OJHw767tnYiXqD86x5rCPT5EGDCRUsJgLAzRrU/BjM'

echo "[WAIT] Waiting for DynamoDB at $ENDPOINT_URL"
until aws dynamodb list-tables --endpoint-url "$ENDPOINT_URL" >/dev/null 2>&1; do
  sleep 1
done

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

create_table_if_not_exists maintenances \
  --table-name maintenances \
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

aws dynamodb put-item \
  --table-name users \
  --item "{
    \"id\": {\"S\": \"$USER_2_ID\"},
    \"name\": {\"S\": \"Giulia Bianchi\"},
    \"email\": {\"S\": \"$USER_2_EMAIL\"},
    \"hashed_password\": {\"S\": \"$USER_HASH\"},
    \"role\": {\"S\": \"USER\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name users \
  --item "{
    \"id\": {\"S\": \"$USER_3_ID\"},
    \"name\": {\"S\": \"Luca Verdi\"},
    \"email\": {\"S\": \"$USER_3_EMAIL\"},
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

aws dynamodb put-item \
  --table-name cars \
  --item "{
    \"id\": {\"S\": \"$CAR_3_ID\"},
    \"plate\": {\"S\": \"IJ789KL\"},
    \"model\": {\"S\": \"Ford Focus\"},
    \"co2_per_km\": {\"N\": \"102.4\"},
    \"status\": {\"S\": \"FREE\"},
    \"mileage\": {
      \"M\": {
        \"km_total\": {\"N\": \"78200\"},
        \"km_servicing\": {\"N\": \"85000\"},
        \"km_wheels\": {\"N\": \"90000\"}
      }
    },
    \"fuel_info\": {
      \"M\": {
        \"type\": {\"S\": \"DIESEL\"},
        \"level\": {\"N\": \"55\"},
        \"card\": {\"S\": \"CARD-003\"}
      }
    }
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name cars \
  --item "{
    \"id\": {\"S\": \"$CAR_4_ID\"},
    \"plate\": {\"S\": \"MN012OP\"},
    \"model\": {\"S\": \"Renault Clio\"},
    \"co2_per_km\": {\"N\": \"91.8\"},
    \"status\": {\"S\": \"IN_USE\"},
    \"mileage\": {
      \"M\": {
        \"km_total\": {\"N\": \"15600\"},
        \"km_servicing\": {\"N\": \"25000\"},
        \"km_wheels\": {\"N\": \"35000\"}
      }
    },
    \"fuel_info\": {
      \"M\": {
        \"type\": {\"S\": \"GASOLINE\"},
        \"level\": {\"N\": \"38\"},
        \"card\": {\"S\": \"CARD-004\"}
      }
    }
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name cars \
  --item "{
    \"id\": {\"S\": \"$CAR_5_ID\"},
    \"plate\": {\"S\": \"QR345ST\"},
    \"model\": {\"S\": \"Peugeot 308\"},
    \"co2_per_km\": {\"N\": \"99.1\"},
    \"status\": {\"S\": \"MAINTENANCE\"},
    \"mileage\": {
      \"M\": {
        \"km_total\": {\"N\": \"61200\"},
        \"km_servicing\": {\"N\": \"61000\"},
        \"km_wheels\": {\"N\": \"65000\"}
      }
    },
    \"fuel_info\": {
      \"M\": {
        \"type\": {\"S\": \"DIESEL\"},
        \"level\": {\"N\": \"25\"},
        \"card\": {\"S\": \"CARD-005\"}
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

aws dynamodb put-item \
  --table-name trips \
  --item "{
    \"id\": {\"S\": \"$TRIP_3_ID\"},
    \"car_id\": {\"S\": \"$CAR_3_ID\"},
    \"user_id\": {\"S\": \"$USER_2_ID\"},
    \"start_position\": {\"S\": \"Torino\"},
    \"end_position\": {\"S\": \"Genova\"},
    \"start_date\": {\"S\": \"2026-05-07T07:45:00+00:00\"},
    \"end_date\": {\"S\": \"2026-05-07T10:20:00+00:00\"},
    \"start_km\": {\"N\": \"78120\"},
    \"end_km\": {\"N\": \"78310\"},
    \"status\": {\"S\": \"closed\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name trips \
  --item "{
    \"id\": {\"S\": \"$TRIP_4_ID\"},
    \"car_id\": {\"S\": \"$CAR_4_ID\"},
    \"user_id\": {\"S\": \"$USER_3_ID\"},
    \"start_position\": {\"S\": \"Bologna\"},
    \"start_date\": {\"S\": \"2026-05-13T06:30:00+00:00\"},
    \"start_km\": {\"N\": \"15600\"},
    \"status\": {\"S\": \"active\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name trips \
  --item "{
    \"id\": {\"S\": \"$TRIP_5_ID\"},
    \"car_id\": {\"S\": \"$CAR_5_ID\"},
    \"user_id\": {\"S\": \"$USER_ID\"},
    \"start_position\": {\"S\": \"Firenze\"},
    \"end_position\": {\"S\": \"Pisa\"},
    \"start_date\": {\"S\": \"2026-05-03T09:15:00+00:00\"},
    \"end_date\": {\"S\": \"2026-05-03T11:05:00+00:00\"},
    \"start_km\": {\"N\": \"60940\"},
    \"end_km\": {\"N\": \"61170\"},
    \"status\": {\"S\": \"closed\"}
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

aws dynamodb put-item \
  --table-name commits \
  --item "{
    \"id\": {\"S\": \"$COMMIT_4_ID\"},
    \"code\": {\"S\": \"COMM-004\"},
    \"description\": {\"S\": \"Consegna documenti Genova\"},
    \"status\": {\"S\": \"DONE\"},
    \"trip_id\": {\"S\": \"$TRIP_3_ID\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name commits \
  --item "{
    \"id\": {\"S\": \"$COMMIT_5_ID\"},
    \"code\": {\"S\": \"COMM-005\"},
    \"description\": {\"S\": \"Sopralluogo Bologna\"},
    \"status\": {\"S\": \"IN_PROGRESS\"},
    \"trip_id\": {\"S\": \"$TRIP_4_ID\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name commits \
  --item "{
    \"id\": {\"S\": \"$COMMIT_6_ID\"},
    \"code\": {\"S\": \"COMM-006\"},
    \"description\": {\"S\": \"Manutenzione programmata sede Firenze\"},
    \"status\": {\"S\": \"DONE\"},
    \"trip_id\": {\"S\": \"$TRIP_5_ID\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name commits \
  --item "{
    \"id\": {\"S\": \"$COMMIT_7_ID\"},
    \"code\": {\"S\": \"COMM-007\"},
    \"description\": {\"S\": \"Attivita da pianificare\"},
    \"status\": {\"S\": \"BACKLOG\"}
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

aws dynamodb put-item \
  --table-name refuelings \
  --item "{
    \"id\": {\"S\": \"$REFUELING_3_ID\"},
    \"date\": {\"S\": \"2026-05-07T07:20:00+00:00\"},
    \"car_id\": {\"S\": \"$CAR_3_ID\"},
    \"liter_price\": {\"N\": \"1.79\"},
    \"liters\": {\"N\": \"46.8\"},
    \"receipt_photo\": {\"S\": \"receipts/$REFUELING_3_ID.jpg\"},
    \"card_number\": {\"S\": \"CARD-003\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name refuelings \
  --item "{
    \"id\": {\"S\": \"$REFUELING_4_ID\"},
    \"date\": {\"S\": \"2026-05-13T06:05:00+00:00\"},
    \"car_id\": {\"S\": \"$CAR_4_ID\"},
    \"liter_price\": {\"N\": \"1.74\"},
    \"liters\": {\"N\": \"28.4\"},
    \"receipt_photo\": {\"S\": \"receipts/$REFUELING_4_ID.jpg\"},
    \"card_number\": {\"S\": \"CARD-004\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name refuelings \
  --item "{
    \"id\": {\"S\": \"$REFUELING_5_ID\"},
    \"date\": {\"S\": \"2026-05-03T08:45:00+00:00\"},
    \"car_id\": {\"S\": \"$CAR_5_ID\"},
    \"liter_price\": {\"N\": \"1.81\"},
    \"liters\": {\"N\": \"35.7\"},
    \"receipt_photo\": {\"S\": \"receipts/$REFUELING_5_ID.jpg\"},
    \"card_number\": {\"S\": \"CARD-005\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

echo "[UPSERT] Maintenances"

aws dynamodb put-item \
  --table-name maintenances \
  --item "{
    \"id\": {\"S\": \"$MAINTENANCE_1_ID\"},
    \"car_id\": {\"S\": \"$CAR_1_ID\"},
    \"date\": {\"S\": \"2026-04-28T09:00:00+00:00\"},
    \"km_at_maintenance\": {\"N\": \"44200\"},
    \"cost\": {\"N\": \"185.50\"},
    \"description\": {\"S\": \"Tagliando olio e filtri\"},
    \"type\": {\"S\": \"ROUTINE_SERVICE\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name maintenances \
  --item "{
    \"id\": {\"S\": \"$MAINTENANCE_2_ID\"},
    \"car_id\": {\"S\": \"$CAR_2_ID\"},
    \"date\": {\"S\": \"2026-05-01T10:30:00+00:00\"},
    \"km_at_maintenance\": {\"N\": \"22600\"},
    \"cost\": {\"N\": \"92.00\"},
    \"description\": {\"S\": \"Controllo freni anteriori\"},
    \"type\": {\"S\": \"BRAKES\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name maintenances \
  --item "{
    \"id\": {\"S\": \"$MAINTENANCE_3_ID\"},
    \"car_id\": {\"S\": \"$CAR_3_ID\"},
    \"date\": {\"S\": \"2026-04-18T15:00:00+00:00\"},
    \"km_at_maintenance\": {\"N\": \"77000\"},
    \"cost\": {\"N\": \"410.00\"},
    \"description\": {\"S\": \"Sostituzione pneumatici estivi\"},
    \"type\": {\"S\": \"TIRES\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name maintenances \
  --item "{
    \"id\": {\"S\": \"$MAINTENANCE_4_ID\"},
    \"car_id\": {\"S\": \"$CAR_5_ID\"},
    \"date\": {\"S\": \"2026-05-04T08:30:00+00:00\"},
    \"km_at_maintenance\": {\"N\": \"61200\"},
    \"cost\": {\"N\": \"260.00\"},
    \"description\": {\"S\": \"Diagnosi motore e reset spie\"},
    \"type\": {\"S\": \"ENGINE\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

aws dynamodb put-item \
  --table-name maintenances \
  --item "{
    \"id\": {\"S\": \"$MAINTENANCE_5_ID\"},
    \"car_id\": {\"S\": \"$CAR_5_ID\"},
    \"date\": {\"S\": \"2026-05-06T11:00:00+00:00\"},
    \"km_at_maintenance\": {\"N\": \"61210\"},
    \"cost\": {\"N\": \"145.00\"},
    \"description\": {\"S\": \"Controllo impianto elettrico\"},
    \"type\": {\"S\": \"ELECTRICAL\"}
  }" \
  --endpoint-url "$ENDPOINT_URL"

echo "[DONE] Local DynamoDB initialized with consistent mock data"
