from common import *  # run from the tools/ folder

def d_markers():
    d=Drawing(DW,165)
    n=10; cw=(DW-40)/n; y=90
    txt(d,DW/2,152,"Partition orders-0, as seen by consumer group “email-service”",8.4,NAVY,font="DVB")
    for i in range(n):
        f=GREEN if i<6 else (ACC if i<8 else colors.HexColor("#F6C89F"))
        d.add(Rect(20+i*cw,y,cw-3,30,rx=3,ry=3,fillColor=f,strokeColor=colors.white)); txt(d,20+i*cw+(cw-3)/2,y+11,str(100+i),7.6,colors.white,font="DVB")
    def mark(i,label,sub,col,yy):
        x=20+i*cw-1.5; d.add(Line(x,y-4,x,yy+14,strokeColor=col,strokeWidth=1.4)); anc="end" if i==10 else "middle"; txt(d,x,yy+2,label,7.6,col,font="DVB",anchor=anc); txt(d,x,yy-9,sub,6.9,GREY,anchor=anc)
    mark(6,"Committed offset = 106","saved in Kafka",GREEN,52)
    mark(8,"Current position = 108","in consumer memory",ACC,18)
    mark(10,"Log-end = 110","next write goes here",NAVY,52)
    txt(d,25,138,"■ processed and committed",7,GREEN,anchor="start"); txt(d,170,138,"■ fetched, not yet committed",7,ACC,anchor="start"); txt(d,330,138,"■ not yet fetched",7,colors.HexColor("#D9894A"),anchor="start")
    return d

def d_crash():
    d=Drawing(DW,175)
    def lane(y,title,steps,col,result,rc):
        txt(d,10,y+34,title,8.2,col,anchor="start",font="DVB")
        bw=(DW-20)/len(steps)
        for i,(t,f,st) in enumerate(steps):
            x=10+i*bw; dbox(d,x,y,bw-8,26,t,f,st,fs=7.2)
            if i<len(steps)-1: arrow(d,x+bw-8,y+13,x+bw,y+13,GREY,w=0.9,head=4)
        txt(d,DW-10,y-12,result,7.6,rc,anchor="end",font="DVB")
    lane(115,"Commit AFTER processing (at-least-once)",[("Poll 100–104",LIGHT,GREY),("Process all 5",GREENL,GREEN),("Crash!",REDL,RED),("Restart at 100",LIGHT,GREY),("Reprocess 100–104",WARM,ACC)],GREEN,"Nothing lost, but duplicates possible → make processing idempotent",ACC)
    lane(40,"Commit BEFORE processing (at-most-once)",[("Poll 100–104",LIGHT,GREY),("Commit 105",WARM,ACC),("Process 100,101",GREENL,GREEN),("Crash!",REDL,RED),("Restart at 105",LIGHT,GREY)],RED,"No duplicates, but 102–104 are lost forever",RED)
    return d

s=[Paragraph("Kafka Day 8",title),Paragraph("Offsets and Commits  ·  Committed Offset vs Position  ·  Auto vs Manual Commit  ·  Consumer Lag  ·  Resetting Offsets",sub),Spacer(1,8),
   box("<b>Today's goal:</b> understand how a consumer remembers where it is, what “committing” really means, and how the timing of a commit decides whether messages can be <b>lost</b> or <b>processed twice</b>. This is one of the most probed Kafka topics in interviews. Allow about 30 minutes.",bg=LIGHT,bar=NAVY),Spacer(1,6)]

s+=[KeepTogether([Paragraph("1. Three positions in a partition",h1n),frame(d_markers()),Paragraph("Figure 1: What the consumer has processed, what it has fetched, and what exists.",cap)]),Spacer(1,4),
    table([["Term","Meaning"],
           ["<b>Log-end offset</b>","The offset the next produced message will get. The “end” of the partition."],
           ["<b>Current position</b>","The next offset this consumer will fetch. Kept in the consumer's memory and moves forward on every poll."],
           ["<b>Committed offset</b>","The position saved in Kafka for this consumer group and partition. After a restart or rebalance, reading resumes from here."],
           ["<b>Consumer lag</b>","Log-end offset − committed offset (here 110 − 106 = 4). How far behind the group is. The key health metric for consumers."]],[34*mm,W-34*mm]),Spacer(1,4),
    box("<b>Important detail:</b> the committed offset is the <b>next</b> message to read, not the last one processed. Processing offset 105 means committing <b>106</b>. Client libraries handle this for you when you commit a message.",bg=WARM,bar=ACC)]

s+=[Paragraph("2. Where are committed offsets stored?",h1),
    Paragraph("In a special internal Kafka topic called <b>__consumer_offsets</b>. Each commit is simply a message saying “group email-service, partition orders-0, offset 106.” It's a compacted topic (Day 13), so Kafka keeps only the latest offset per group and partition. Very old Kafka versions stored offsets in ZooKeeper instead.",body)]

s+=[Paragraph("3. Auto commit (the default)",h1),
    table([["Setting","Default","Meaning"],
           [M("enable.auto.commit"),"true","Commit automatically in the background"],
           [M("auto.commit.interval.ms"),"5000","Commit roughly every 5 seconds, during poll()"]],[60*mm,22*mm,W-82*mm]),Spacer(1,4),
    Paragraph("Auto commit commits what the consumer has <b>fetched</b>, not what it has finished processing. That's fine if you fully process each batch before the next poll, but it causes two problems:",body),Spacer(1,3),
    table([["Risk","How it happens"],
           ["<b>Duplicates</b>","You process messages, then crash before the next auto commit. On restart, the group resumes from the last commit and processes them again."],
           ["<b>Lost messages</b>","You hand messages to background threads and poll again. Auto commit marks them done; if the app crashes before the threads finish, they're never processed."]],[30*mm,W-30*mm])]

s+=[KeepTogether([Paragraph("4. Manual commit: you decide when",h1n),
    Paragraph("Set "+M("enable.auto.commit=false")+" and commit yourself. <b>When</b> you commit decides your delivery guarantee:",body),Spacer(1,4),
    frame(d_crash()),Paragraph("Figure 2: The same crash with two commit strategies.",cap)]),Spacer(1,4),
    table([["","commitSync","commitAsync"],
           ["<b>Behavior</b>","Waits for Kafka to confirm; retries on failure","Sends and continues; doesn't retry"],
           ["<b>Speed</b>","Slower (blocks)","Faster"],
           ["<b>Typical use</b>","On shutdown and before a rebalance","In the normal processing loop"]],[30*mm,(W-30*mm)/2,(W-30*mm)/2]),Spacer(1,4),
    Paragraph("A common pattern: <b>commitAsync</b> after each batch for speed, plus <b>commitSync</b> on shutdown so the final position is saved for sure. Committing after every single message is safest but slow; committing per batch is the usual balance.",body)]

s+=[Paragraph("5. auto.offset.reset: when there's no committed offset",h1),
    table([["Value","When the group has no saved offset (new group, or offset expired)"],
           [M("latest")+" (default)","Start from new messages only. Old data is skipped."],
           [M("earliest"),"Start from the oldest available message. Good for a new service that needs history."],
           [M("none"),"Throw an error, forcing you to decide explicitly."]],[34*mm,W-34*mm]),Spacer(1,4),
    Paragraph("It only applies when there's <b>no valid committed offset</b>. Once a group has committed, it always resumes from there.",small)]

s+=[Paragraph("6. Seeing lag and resetting offsets",h1),
    code("# Check where a group is and how far behind it is\nkafka-consumer-groups.sh --bootstrap-server localhost:9092 \\\n  --describe --group email-service\n\nTOPIC   PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG\norders  0          106             110             4\norders  1          88              88              0\n\n# Replay from a point in time (stop the group's consumers first)\nkafka-consumer-groups.sh --bootstrap-server localhost:9092 \\\n  --group email-service --topic orders \\\n  --reset-offsets --to-datetime 2026-11-24T10:00:00.000 --execute"),Spacer(1,3),
    Paragraph("Without --execute, the reset command only shows what it would do (a dry run). Other options include --to-earliest, --to-latest, and --shift-by -100.",small)]

s+=[Paragraph("7. Code: manual commit after processing",h1),
    Paragraph("<b>Python</b> (confluent-kafka)",h3),
    code("c = Consumer({\"bootstrap.servers\": \"localhost:9092\", \"group.id\": \"email-service\",\n              \"enable.auto.commit\": False, \"auto.offset.reset\": \"earliest\"})\nc.subscribe([\"orders\"])\ntry:\n    while True:\n        msg = c.poll(1.0)\n        if msg is None or msg.error():\n            continue\n        send_email(msg.value())                    # process first\n        c.commit(message=msg, asynchronous=True)   # then commit offset + 1\nfinally:\n    c.commit(asynchronous=False)                   # final sync commit\n    c.close()"),
    Paragraph("<b>Java</b>",h3),
    code("props.put(\"enable.auto.commit\", \"false\");\ntry {\n    while (running) {\n        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(500));\n        for (ConsumerRecord<String, String> r : records) sendEmail(r.value());\n        consumer.commitAsync();          // commit the whole batch\n    }\n} finally {\n    consumer.commitSync();               // make sure the last position is saved\n    consumer.close();\n}")]

s+=[Paragraph("8. Common mistakes",h1),
    table([["Mistake","What goes wrong","Better"],
           ["Auto commit with async processing","Messages marked done before they're processed → lost on crash","Disable auto commit; commit after processing"],
           ["Committing before processing","At-most-once: crashes lose messages","Commit after processing, unless loss is acceptable"],
           ["Assuming no duplicates","At-least-once delivery redelivers after crashes","Make consumers idempotent (Day 17)"],
           ["Expecting auto.offset.reset to replay","It's ignored once offsets exist","Use kafka-consumer-groups --reset-offsets"],
           ["Never monitoring lag","Consumers silently fall behind until data expires","Alert on consumer lag"]],[42*mm,(W-42*mm)/2,(W-42*mm)/2])]

Q=[("What is a consumer offset, and where is it stored?",
    "An offset is a message's position in a partition. Each consumer group commits the offset of the next message it should read for each partition, and Kafka stores these commits in the internal __consumer_offsets topic. After a restart or rebalance, consumers resume from the committed offset.",
    "Very common",None),
   ("What happens if a consumer crashes after processing a message but before committing?",
    "On restart, the group resumes from the last committed offset, so that message is processed again. This is at-least-once delivery, and it's why consumers should be idempotent, for example by recording processed event IDs.",
    "Very common","“How would you avoid sending a customer two emails?” (Store processed event IDs and skip repeats; Day 17.)"),
   ("Auto commit vs manual commit: what's the difference and when would you use each?",
    "Auto commit saves the fetched position every few seconds in the background, which is simple but can cause duplicates, or lost messages when processing is asynchronous. Manual commit lets you commit only after processing succeeds, giving at-least-once guarantees. I'd use manual commit for anything important, like payments or orders.",
    "Common",None),
   ("What is consumer lag and why does it matter?",
    "Lag is the difference between the partition's latest offset and the group's committed offset: how many messages are waiting. Growing lag means consumers can't keep up; if it lasts longer than retention, data is lost to them. It's the main metric to monitor and alert on.",
    "Common",None),
   ("What does auto.offset.reset do?",
    "It decides where a consumer starts when its group has no valid committed offset: latest (only new messages, the default), earliest (from the oldest available), or none (raise an error). It doesn't apply once a valid offset exists.",
    "Common",None)]
for i,(q,a,l,f) in enumerate(Q,1):
    if i==1: s.append(KeepTogether([Paragraph("9. Interview questions",h1n),Paragraph("Labels show how often each is asked.",small),Spacer(1,4),qa_l(i,q,a,l,f)]))
    else: s.append(qa_l(i,q,a,l,f))

S=[("After a deployment, some customers got two order-confirmation emails. Logs show the email consumer restarted mid-batch. What happened, and how do you fix it?",
    "The consumer processed part of a batch, then restarted before committing, so it resumed from the last committed offset and resent those emails. That's expected at-least-once behavior. Fix it by making the consumer idempotent: store each event ID after sending and skip IDs already seen. Committing more often (smaller batches) reduces how many repeat, but idempotency is the real fix.",None),
   ("A new consumer group for an analytics service starts and receives only today's events, but it needed the last 5 days. Why?",
    "With no committed offsets, auto.offset.reset applied, and its default is latest, so it started from new messages. It should have been set to earliest before the first start. Since the group now has offsets, changing the setting won't help; reset its offsets with kafka-consumer-groups --reset-offsets (to earliest or a date) while it's stopped.",None)]
for i,(q,a,f) in enumerate(S,1):
    if i==1: s.append(KeepTogether([Paragraph("10. Situation-based scenarios",h1n),Paragraph("Answer as <b>problem → solution → trade-off</b>.",small),Spacer(1,4),qa(i,q,a,f)]))
    else: s.append(qa(i,q,a,f))

quiz=[("You processed offset 41. What offset gets committed?","42, the next message to read."),
      ("Where does Kafka store committed offsets?","In the internal __consumer_offsets topic."),
      ("Commit after processing gives which guarantee?","At-least-once (possible duplicates, no loss)."),
      ("Log-end offset 500, committed 470. What's the lag?","30 messages."),
      ("A group already has offsets. Will setting auto.offset.reset=earliest make it replay?","No. Use kafka-consumer-groups --reset-offsets.")]
s+=[KeepTogether([Paragraph("11. Self-check quiz",h1n),Paragraph("Cover the answers and test yourself. If you miss two or more, reread sections 1, 3 and 4.",small),Spacer(1,3),table([["Question","Answer (cover this column first)"]]+[[a,b] for a,b in quiz],[W*0.5,W*0.5])])]

s+=[KeepTogether([Paragraph("12. Recap",h1n),
    table([["Remember","In one line"],
           ["Committed offset","Next message to read, saved per group and partition"],
           ["Stored in","__consumer_offsets (compacted internal topic)"],
           ["Lag","Log-end offset − committed offset; monitor it"],
           ["Auto commit","Default every 5 s; can duplicate or lose with async processing"],
           ["Commit after processing","At-least-once → make consumers idempotent"],
           ["Commit before processing","At-most-once → possible loss"],
           ["commitAsync / commitSync","Fast in the loop / safe on shutdown"],
           ["auto.offset.reset","latest (default), earliest, none; only without saved offsets"],
           ["Replay","kafka-consumer-groups --reset-offsets (group stopped)"]],[40*mm,W-40*mm]),Spacer(1,8),
    box("<b>Tomorrow's warm-up recall:</b> draw the three positions (committed, current, log-end), explain what happens on a crash with commit-before vs commit-after, and define lag.<br/><b>Next: Kafka Day 9</b>: consumer groups and rebalancing.",bg=LIGHT,bar=NAVY)])]

out="/mnt/user-data/outputs/Kafka_Day8_Offsets_and_Commits.pdf"
build(out,"Kafka Day 8 · Offsets and Commits",s)
print(preview(out,"k8"))
