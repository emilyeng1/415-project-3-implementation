[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/8IqmWj30)

How to run dashboard:

 Requirements:
 - have the virtual environment open with:
    "source env/dev/bin/activate"
 - two terminals

 In one terminal, run the command "uvicorn main:app --reload"
 In the other terminal (after cd to frontend), run "npm run build" and then "npm start"
 
 Once the message for viewing the dashboard appears, open
 http://localhost:3001
 and enter a query for the API to process.


| Sample Query | Expected Output |
| --- | --- |
| SELECT subreddit, post_title, toxicity_score, data::json->>'selftext' AS selftext FROM posts WHERE (post_title ILIKE '%climate%' AND post_title ILIKE '%election%') OR (data::json->>'selftext' ILIKE '%climate%' AND data::json->>'selftext' ILIKE '%election%') LIMIT 5  | table of post title, toxicity score, and post content from Reddit posts database where the title includes the words 'climate' and 'election' OR the post's contents include the words 'climate' and 'election' |
| SELECT comment_body, toxicity_score FROM comments WHERE toxicity_score = 'flag' | all flagged comments in the Reddit comments database in a table containing the comment itself and its toxicity score |
| SELECT comment_body, toxicity_score FROM comments WHERE (comment_body ILIKE '%climate%' AND comment_body ILIKE '%election%') LIMIT 5 | table of comment body and toxicity score of at most 5 Reddit comments from the database that include the words 'climate' and 'election' |
| SELECT comment_body, toxicity_score FROM comments WHERE (comment_body ILIKE '%climate%' AND comment_body ILIKE '%trump%') LIMIT 5 | table of comment body and toxicity score of at most 5 Reddit comments from the database that include the words 'climate' and 'trump' |
| SELECT board, thread_number, post_number, toxicity_score FROM posts WHERE toxicity_score = 'normal' LIMIT 5 | table of at most 5 board, thread number, post number, and toxicity score from the 4chan posts database where the toxicity score is normal |
| SELECT board, thread_number, data, toxicity_score FROM posts WHERE toxicity_score = 'flag' LIMIT 5 | table of at most 5 board, thread number, post data, and toxicity score from the 4chan posts database where the toxicity score is flag |

Attached is also a commands document (cmds.pdf) where Emily has taken note of most of the commands run for project 1 as well as:
- how to use screen
- issues run into while testing
- the sample queries shown above
