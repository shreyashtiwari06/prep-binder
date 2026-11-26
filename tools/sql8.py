from common import *  # run from the tools/ folder

def d_corr():
    d=Drawing(DW,165)
    txt(d,DW/2,152,"For EACH employee row, the inner query runs with that row's department",8.4,NAVY,font="DVB")
    rows=[("Asha","Sales","90k","avg Sales = 70k","✓"),("Ravi","Sales","50k","avg Sales = 70k","✗"),("Neha","IT","95k","avg IT = 85k","✓"),("Amit","IT","75k","avg IT = 85k","✗")]
    for i,(n,dp,sal,avg,ok) in enumerate(rows):
        y=120-i*28
        dbox(d,10,y,150,22,f"{n} · {dp} · {sal}",BLUEL,NAVY,fs=7.6)
        arrow(d,160,y+11,190,y+11,GREY,w=0.9,head=4)
        dbox(d,192,y,175,22,f"inner query → {avg}",WARM,ACC,fs=7.4)
        good=ok=="✓"
        txt(d,400,y+7,"keep" if good else "skip",8,GREEN if good else RED,font="DVB",anchor="start")
    txt(d,DW/2,6,"Logically one inner run per outer row. Modern databases often optimize this, but think of it this way.",7.2,GREY,font="DVI")
    return d

def d_exists():
    d=Drawing(DW,110)
    dbox(d,10,48,120,40,"Customer: Asha",BLUEL,NAVY,fs=8)
    arrow(d,130,68,165,68,GREY)
    for i,o in enumerate(["order 101","order 102","order 103"]):
        x=170+i*75; f,st=(GREENL,GREEN) if i==0 else (FADE,colors.HexColor("#BBBBBB"))
        dbox(d,x,52,68,32,o,f,st,fs=7.6,tc=colors.black if i==0 else colors.HexColor("#999"))
    txt(d,204,40,"match found →",7.4,GREEN,font="DVB"); txt(d,204,29,"EXISTS = TRUE",7.4,GREEN,font="DVB")
    txt(d,315,40,"never checked:",7.4,GREY); txt(d,315,29,"stops at the first match",7.4,GREY)
    txt(d,DW/2,8,"EXISTS only asks “is there at least one?”, so it can stop early and never returns duplicates.",7.4,NAVY,font="DVI")
    return d

s=[Paragraph("SQL Day 8",title),Paragraph("Correlated Subqueries  ·  EXISTS and NOT EXISTS  ·  EXISTS vs IN vs JOIN",sub),Spacer(1,8),
   box("<b>Today's goal:</b> understand subqueries that depend on the outer row, how EXISTS works, and how to choose between EXISTS, IN and JOIN, including the NULL and duplicate traps interviewers love.",bg=LIGHT,bar=NAVY),Spacer(1,6)]

s+=[KeepTogether([Paragraph("1. What makes a subquery “correlated”?",h1n),
    Paragraph("Yesterday's subqueries ran <b>once</b>. A <b>correlated</b> subquery refers to a column from the outer query, so its result changes for each outer row.",body),Spacer(1,4),
    code("-- Employees who earn more than their own department's average\nSELECT e.name, e.dept, e.salary\nFROM employees e\nWHERE e.salary > (SELECT AVG(e2.salary)\n                  FROM employees e2\n                  WHERE e2.dept = e.dept);   -- e.dept comes from the outer row"),Spacer(1,4),
    frame(d_corr()),Paragraph("Figure 1: The inner query is re-evaluated for each outer row.",cap)]),Spacer(1,4),
    table([["","Non-correlated (Day 7)","Correlated (today)"],
           ["<b>References the outer query?</b>","No","Yes"],
           ["<b>Runs</b>","Once","Logically once per outer row"],
           ["<b>Can run on its own?</b>","Yes","No: it needs a value from the outer row"],
           ["<b>Performance</b>","Usually cheap","Can be slow on large tables; often rewritten by the optimizer, or by you with a JOIN or window function"]],[40*mm,(W-40*mm)/2,(W-40*mm)/2])]

s+=[KeepTogether([Paragraph("2. EXISTS and NOT EXISTS",h1n),
    Paragraph("EXISTS is the most common use of a correlated subquery. It returns TRUE if the inner query finds <b>at least one row</b>; what it selects doesn't matter, so people write "+M("SELECT 1")+".",body),Spacer(1,4),
    code("-- Customers who have placed at least one order\nSELECT c.name FROM customers c\nWHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);\n\n-- Customers who have never ordered (anti-join, Day 6)\nSELECT c.name FROM customers c\nWHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);"),Spacer(1,4),
    frame(d_exists()),Paragraph("Figure 2: EXISTS stops as soon as it finds one match.",cap)])]

s+=[Paragraph("3. EXISTS vs IN vs JOIN",h1),
    table([["","EXISTS","IN","JOIN"],
           ["<b>Question it answers</b>","Is there a matching row?","Is the value in this list?","Combine columns from both tables"],
           ["<b>Duplicates in result</b>","Never: each outer row appears once","Never","Yes, if one row matches many (needs DISTINCT)"],
           ["<b>NULLs</b>","NOT EXISTS is safe","NOT IN breaks if the list contains NULL","LEFT JOIN + IS NULL is safe"],
           ["<b>Good for</b>","Correlated checks against large tables","Small or fixed lists: IN ('A','B')","When you need the other table's columns"],
           ["<b>Performance</b>","Stops at first match","Similar for subqueries in modern optimizers","Usually efficient with indexes"]],[30*mm,(W-30*mm)/3,(W-30*mm)/3,(W-30*mm)/3]),Spacer(1,4),
    box("<b>The duplicate trap:</b> “customers who ordered” written as a JOIN returns Asha twice if she has two orders, and you'd need DISTINCT. EXISTS returns her once, naturally. When you only need to <b>check</b> for related rows, EXISTS is the cleaner, more correct choice.",bg=WARM,bar=ACC)]

s+=[Paragraph("4. Rewriting correlated subqueries",h1),
    Paragraph("Interviewers sometimes ask you to rewrite a slow correlated subquery. The usual trick is to compute the per-group values once, then join:",body),Spacer(1,4),
    code("-- Same result as section 1, but the averages are computed once per department\nSELECT e.name, e.dept, e.salary\nFROM employees e\nJOIN (SELECT dept, AVG(salary) AS avg_sal\n      FROM employees GROUP BY dept) d ON d.dept = e.dept\nWHERE e.salary > d.avg_sal;"),Spacer(1,3),
    Paragraph("Window functions (Day 11) offer a third way: "+M("AVG(salary) OVER (PARTITION BY dept)")+".",small)]

s+=[KeepTogether([Paragraph("5. Today's practice: LeetCode 1045 – Customers Who Bought All Products",h1n),
    box("<b>Task:</b> find customers who bought every product in the Product table.<br/><b>Hint:</b> for each customer, count the distinct products they bought, and compare with the total number of products, which a scalar subquery can give you inside HAVING.<br/><b>Advanced (impressive in interviews):</b> the same question can be answered with a double NOT EXISTS: “there is no product that this customer has not bought.” Try writing it.",bg=WARM,bar=ACC)])]

Q=[("What is a correlated subquery?",
    "A subquery that references a column from the outer query, so it's evaluated for each outer row, like comparing each employee's salary with their own department's average. It can't run on its own. It can be slow on large tables, so it's often rewritten as a JOIN to a grouped subquery or with a window function.",
    "Common",None),
   ("When would you use EXISTS instead of IN?",
    "EXISTS for correlated checks like “customers who have orders,” especially against large tables, since it stops at the first match and never duplicates rows. IN suits small or fixed lists. For the negative case, NOT EXISTS is safer than NOT IN, which returns nothing if the subquery yields a NULL.",
    "Very common","“Is EXISTS always faster?” (Not necessarily; modern optimizers often plan IN and EXISTS the same way, so check the plan.)"),
   ("Why might a JOIN return more rows than an EXISTS query for the same question?",
    "A JOIN returns one row per matching pair, so a customer with three orders appears three times. EXISTS only checks whether any match exists, so each customer appears once. You'd need DISTINCT with the JOIN, which adds work.",
    "Common",None),
   ("How would you speed up a slow correlated subquery?",
    "Compute the per-group values once in a grouped subquery or CTE and join to it, or use a window function. Also make sure the column the subquery filters on is indexed, and check the execution plan.",
    "Good to know",None)]
for i,(q,a,l,f) in enumerate(Q,1):
    if i==1: s.append(KeepTogether([Paragraph("6. Interview questions",h1n),Paragraph("Labels show how often each is asked.",small),Spacer(1,4),qa_l(i,q,a,l,f)]))
    else: s.append(qa_l(i,q,a,l,f))

s+=[KeepTogether([Paragraph("7. Situation-based scenario",h1n),Paragraph("Answer as <b>problem → solution → trade-off</b>.",small),Spacer(1,4),
    qa(1,"A “customers who ordered this month” list shows some customers several times, and the count of customers looks too high. The query joins customers to orders. Fix it.",
    "Customers with several orders this month appear once per order because of the join. Since we only need to know whether they ordered, rewrite it with EXISTS and the date condition inside the subquery; each customer appears once and the count becomes correct. COUNT(DISTINCT c.id) on the join would also work, but EXISTS states the intent more clearly.",None)])]

s+=[KeepTogether([Paragraph("8. Recap",h1n),
    table([["Remember","In one line"],
           ["Correlated subquery","Uses an outer column; logically runs per outer row"],
           ["EXISTS","TRUE if at least one row; stops at first match; SELECT 1"],
           ["NOT EXISTS","Safest anti-join; NULLs don't break it"],
           ["IN","Good for small or fixed lists; NOT IN + NULL = no rows"],
           ["JOIN vs EXISTS","JOIN can duplicate; EXISTS never does"],
           ["Speeding up","Grouped subquery + JOIN, window function, index"]],[36*mm,W-36*mm]),Spacer(1,8),
    box("<b>Tomorrow's warm-up recall:</b> write “employees earning more than their department's average” from memory, and explain when EXISTS beats IN and JOIN.<br/><b>Next: SQL Day 9</b>: UNION vs UNION ALL.",bg=LIGHT,bar=NAVY)])]

out="/mnt/user-data/outputs/SQL_Day8_Correlated_Subqueries_EXISTS.pdf"
build(out,"SQL Day 8 · Correlated Subqueries and EXISTS",s)
print(preview(out,"s8"))
