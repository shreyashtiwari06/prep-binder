from common import *  # run from the tools/ folder
def q(t): return f"<i>Interview Q: “{t}”</i>"
days=[
("Day 1","Mon, Nov 23","",[
 ("Recall","<b>From Friday:</b> Longest Consecutive Sequence · Dependency Inversion/Injection · Kafka message keys and schemas · SELF JOIN.<br/><b>Older:</b> Next Permutation."),
 ("DSA","Set Matrix Zeroes, Rotate Matrix by 90°"),("Mystery","LeetCode 881 – Boats to Save People (Medium)"),
 ("LLD","<b>DRY, KISS, YAGNI, Law of Demeter.</b> What each means, a code smell that breaks it, and the fix.<br/>Practice: refactor a method chain like "+M("order.getCustomer().getAddress().getCity()")+".<br/>"+q("What is the Law of Demeter and why does it matter?")),
 ("Kafka","<b>Day 6: Core architecture.</b> Broker, cluster, topic, partition, producer, consumer; how a message flows end to end; why consumers pull.<br/>"+q("Walk me through what happens when a producer sends a message.")),
 ("SQL","<b>Day 6: CROSS JOIN and finding missing rows.</b> Cartesian products; LEFT JOIN + IS NULL (anti-join).<br/>Practice: 1581 Customer Who Visited but Did Not Make Any Transactions.<br/>"+q("Find customers who never placed an order."))]),
("Day 2","Tue, Nov 24","",[
 ("Recall","<b>From Monday:</b> Set Matrix Zeroes, Rotate Matrix, Boats to Save People · DRY/KISS/YAGNI · Kafka architecture · anti-join.<br/><b>Older:</b> Majority Element."),
 ("DSA","Spiral Traversal of a Matrix, Count Subarray Sum Equals K"),
 ("LLD","<b>Singleton.</b> When to use it, lazy vs eager creation, the thread-safe version, and why it's often called an anti-pattern.<br/>"+q("How do you make a Singleton thread-safe?")),
 ("Kafka","<b>Day 7: Partitions.</b> Why topics are split; key → partition; ordering per partition; hot partitions; choosing partition count.<br/>"+q("How would you guarantee ordering for all events of one user?")),
 ("SQL","<b>Day 7: Subqueries.</b> In WHERE, FROM and SELECT; scalar vs list subqueries.<br/>Practice: 1978 Employees Whose Manager Left the Company.<br/>"+q("Find the second highest salary."))]),
("Day 3","Wed, Nov 25","",[
 ("Recall","<b>From Tuesday:</b> Spiral Traversal, Count Subarray Sum Equals K · Singleton · partitions · subqueries.<br/><b>Older:</b> Kadane's / Buy and Sell Stock."),
 ("DSA","Pascal's Triangle, Majority Element II"),("Mystery","LeetCode 1695 – Maximum Erasure Value (Medium)"),
 ("LLD","<b>Factory Method.</b> Moving object creation out of business code; when a simple factory is enough.<br/>Practice: a NotificationFactory that returns Email, SMS or Push senders.<br/>"+q("What problem does the Factory pattern solve?")),
 ("Kafka","<b>Day 8: Offsets and commits.</b> Committed offset vs current position; auto vs manual commit; what happens on restart.<br/>"+q("What happens if a consumer crashes after processing but before committing?")),
 ("SQL","<b>Day 8: Correlated subqueries, EXISTS vs IN.</b> How a correlated subquery runs per row; NOT EXISTS vs NOT IN with NULLs.<br/>Practice: 1045 Customers Who Bought All Products.<br/>"+q("When would you use EXISTS instead of IN?"))]),
("Day 4","Thu, Nov 26","Hard day: 1 problem",[
 ("Recall","<b>From Wednesday:</b> Pascal's Triangle, Majority Element II, Maximum Erasure Value · Factory Method · offsets · EXISTS vs IN.<br/><b>Older:</b> Rearrange by Sign / Leaders."),
 ("DSA","3 Sum"),
 ("LLD","<b>Abstract Factory.</b> Creating families of related objects; how it differs from Factory Method.<br/>Practice: a UI kit with Light and Dark themes (Button, Checkbox).<br/>"+q("Factory Method vs Abstract Factory: what's the difference?")),
 ("Kafka","<b>Day 9: Consumer groups and rebalancing.</b> How partitions are shared; more consumers than partitions; what triggers a rebalance.<br/>"+q("You have 3 partitions and 5 consumers in one group. What happens?")),
 ("SQL","<b>Day 9: UNION vs UNION ALL.</b> Removing duplicates vs keeping them; column rules; performance.<br/>Practice: 1789 Primary Department for Each Employee.<br/>"+q("Why is UNION ALL usually faster than UNION?"))]),
("Day 5","Fri, Nov 27","Hard day: 1 problem",[
 ("Recall","<b>From Thursday:</b> 3 Sum · Abstract Factory · consumer groups · UNION vs UNION ALL.<br/><b>Older:</b> Next Permutation."),
 ("DSA","4 Sum"),
 ("Revision","<b>Weekly revision (30 min):</b> redo problems you couldn't recall, skim the week's one-line insights, and ask Claude for a quiz on this week's LLD, Kafka and SQL."),
 ("Mystery","LeetCode 523 – Continuous Subarray Sum (Medium)"),
 ("LLD","<b>Builder.</b> Building objects with many optional fields step by step; immutable results.<br/>Practice: a Pizza or HttpRequest builder.<br/>"+q("When would you choose Builder over a constructor?")),
 ("Kafka","<b>Day 10: Replication.</b> Leader and follower replicas, replication factor, in-sync replicas (ISR), what happens when a broker dies.<br/>"+q("How does Kafka avoid losing data when a broker fails?")),
 ("SQL","<b>Day 10: CASE WHEN and conditional aggregation.</b> Labels, buckets, and counting by condition in one query.<br/>Practice: 1934 Confirmation Rate.<br/>"+q("Count paid and unpaid orders per customer in one query."))]),
]
def card(d):
    name,date,tag,rows=d
    extra=f"   <font size='9' color='#F6C89F'>{tag}</font>" if tag else ""
    hdr=Table([[Paragraph(f"{name}  <font color='#F6C89F'>|</font>  {date}{extra}",ParagraphStyle("dh",fontName="DVB",fontSize=12,leading=15,textColor=colors.white))]],colWidths=[W])
    hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),NAVY),("LEFTPADDING",(0,0),(-1,-1),10),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    t=Table([[Paragraph(k,lab),Paragraph(v,body)] for k,v in rows],colWidths=[22*mm,W-22*mm])
    st=[("VALIGN",(0,0),(-1,-1),"TOP"),("LINEBELOW",(0,0),(-1,-2),0.5,LINE),("BOX",(0,0),(-1,-1),0.6,LINE),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("BACKGROUND",(0,0),(0,-1),LIGHT)]
    for i,(k,_) in enumerate(rows):
        if k in ("Mystery","Revision"): st.append(("BACKGROUND",(1,i),(1,i),WARM))
    t.setStyle(TableStyle(st)); return KeepTogether([hdr,t,Spacer(1,9)])
s=[Paragraph("Interview Prep · Week 3",title),Paragraph("Nov 23 – Nov 29  ·  DSA (A2Z arrays) · LLD (principles + creational patterns) · Kafka Days 6–10 · SQL Days 6–10 · API concepts",sub),Spacer(1,8),
   table([["Block","Time"],["Recall warm-up","10 min"],["DSA: 2 A2Z problems (1 on hard days)","60 min"],["LLD topic","25 min"],["Kafka: one topic in depth","30 min"],["SQL: 1 concept + 1 problem","10 min"],["Mystery Pattern (Mon, Wed, Fri)","15 min"]],[W-35*mm,35*mm]),Spacer(1,4),
   Paragraph("<i>About 2 hrs 15 min most days, 2 hrs 30 min on Mystery days. Friday has 1 new DSA problem plus weekly revision.</i>",small),Spacer(1,6),
   box("<b>This week's focus:</b> finish the A2Z array matrix and sum problems; LLD moves from principles into <b>creational design patterns</b>; Kafka reaches the core internals (architecture, partitions, offsets, consumer groups, replication); SQL covers anti-joins, subqueries and conditional logic. Notes PDFs for Kafka and SQL appear on the site each day when you ask for them.",bg=LIGHT,bar=NAVY),Spacer(1,10)]
for d in days: s.append(card(d))
wk=[("Sat: API design (45 min)","Resource naming, nested resources, versioning, pagination (offset vs cursor), filtering and sorting.<br/>"+q("When would you use cursor-based pagination over offset?")),
    ("Sun: Request handling (45 min)","Validation (Pydantic / Bean Validation), consistent error responses, DTOs vs entities, how a request flows through FastAPI and Spring Boot.<br/>"+q("Why shouldn't you return database entities directly from an API?")),
    ("Optional","Catch up on anything pending first. Mystery bonus: LeetCode 18 – 4Sum II style practice is not needed; instead redo one problem you found hard.")]
hdr=Table([[Paragraph("Sat–Sun, Nov 28–29  ·  Backlog + API Concepts",ParagraphStyle("dh2",fontName="DVB",fontSize=12,leading=15,textColor=colors.white))]],colWidths=[W]); hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),ACC),("LEFTPADDING",(0,0),(-1,-1),10),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
wt=Table([[Paragraph(k,lab),Paragraph(v,body)] for k,v in wk[:2]],colWidths=[36*mm,W-36*mm]); wt.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LINEBELOW",(0,0),(-1,-2),0.5,LINE),("BOX",(0,0),(-1,-1),0.6,LINE),("LEFTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("BACKGROUND",(0,0),(0,-1),LIGHT)]))
s.append(KeepTogether([hdr,wt,Spacer(1,8),box("<b>Mystery Pattern reminder:</b> before coding, spend 2 minutes deciding whether it's two pointers, hashing, or sliding window, post your reasoning in the group, then solve.",bg=WARM,bar=ACC)]))
out="/mnt/user-data/outputs/Interview_Prep_Week3_Nov23-29.pdf"
build(out,"Interview Prep · Week 3 (Nov 23 – Nov 29)",s)
print(preview(out,"w3"))
