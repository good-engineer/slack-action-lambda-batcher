# slack-action-lambda-batcher

process: 

everyday morning lambda batcher loads new orders and send them to slack channel
<img width="570" alt="Screen Shot 2021-11-25 at 10 55 10 AM" src="https://user-images.githubusercontent.com/19164143/143364485-56b5d884-fadd-4f55-8a64-6f84f7fbd369.png">

the admins can press start btn to change the order status to started
on pressing the btn slack will trigger the django api server that will change the order status and
send back the response to slack to update the start btn to complete btn
<img width="545" alt="Screen Shot 2021-11-25 at 10 55 23 AM" src="https://user-images.githubusercontent.com/19164143/143364491-947a73e2-f8d5-4a1f-a3ca-b2a52379efa9.png">

after completeing the order admin from channel can press complete btn 
as mentioned above the slcak will trigger the django api server to update the status and 
send back the response to slack to update the complete btn to order complete/failed status
<img width="580" alt="Screen Shot 2021-11-25 at 10 55 00 AM" src="https://user-images.githubusercontent.com/19164143/143364502-5a0e04eb-137c-4fbe-8090-0ccee51a6962.png">

* on pressing btn the admin slack id is also sent to server and will be displayed on the order msg in slack channel
