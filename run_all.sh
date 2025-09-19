
dates=("2025-01-01" "2025-03-01" "2025-05-01" "2025-07-01" "2025-09-01")


BASE=USD
TARGET=EUR

for date in "${dates[@]}"; do
    python lab02/currency_exchange_rate.py $BASE $TARGET $date
done
