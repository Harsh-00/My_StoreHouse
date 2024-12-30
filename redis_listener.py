import time
from database import redis
from models import Product

key="order-completed"
group="order-completed-group"

# Create a group
try:
    redis.xgroup_create(name=key,groupname=group,mkstream=True)
    print(f"Created group {group}")
except Exception as e:
    print(str(e))
    print(f"Group {group} already exists")

# Listen for new messages
# key:">" means listen for all messages
while True:
    try:
        result=redis.xreadgroup(groupname=group,consumername=key,streams={key:">"} )
        print(result)
        if result:
            for res in result:
                obj=res[1][0][1]
                try:
                    product=Product.get(obj["product_id"])
                    
                    if product.quantity<int(obj["quantity"]): 
                        raise Exception("Not enough stock")
                    else:
                        product.quantity-=int(obj["quantity"]) 

                    product.save()
                    print(product.dict())
                except Exception as e:
                    redis.xadd(name="refund-order",fields=obj)

    except Exception as e:
        print(str(e))
    time.sleep(3)
