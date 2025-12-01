from configparser import ConfigParser
import httpx   
import openai
import base64   

class Gpt4ifxAPI:
    def __init__(self):
        self.configur = ConfigParser()
        self.configur.read('config.ini')

        self.cert_path = 'ca-bundle.crt'
        self.Gpt4ifxchatUrl = self.configur.get('gpt4ifxapi', 'chaturl')
        self.Gpt4ifxUname = self.configur.get('gpt4ifxapi', 'username')
        self.Gpt4ifxPassword = self.configur.get('gpt4ifxapi', 'password')

        sample_string = self.Gpt4ifxUname + ":" + self.Gpt4ifxPassword   
        sample_string_bytes = sample_string.encode("ascii")   
    
        base64_bytes = base64.b64encode(sample_string_bytes)   
        self.BasicToken = base64_bytes.decode("ascii")   
    
              
        self.headers = {     
                    'Authorization': f"Basic {self.BasicToken}",      
                    "accept": "application/json",
                    "Content-Type": "application/json"
                }

        self.Gpt4ifxBearertoken = self.configur.get('gpt4ifxapi', 'bearertoken')
        self.Gpt4ifxUrlBearertoken = self.configur.get('gpt4ifxapi', 'url_bearertoken')
        self.Gpt4ifxmodel = self.configur.get('gpt4ifxapi', 'model')
        self.kbaprompt = """Please help me to write a Knowledge Base Article (KBA).\
    Please act as a product engineer with 25 years of experience and deep knowledge in the area of semiconductors in general, and Infineon products in particular.\
    The topic of the KBA is provided by the user input.\
    \
    The KBA is written for fellow engineers, so it should be technically sound and informative at a deep knowledge level. The KBA should be concise. After reading, the engineer should feel well informed and wants to give positive feedback on the KBA. The language used is clear, eloquent, and technically precise.\
    Use the following structure for the KBA:\
    \
    [Title: Start with a title that includes the specific product name and the problem, error message or key question. Use relevant focus keywords for Search-Engine Optimization (SEO). Do not exceed 70 characters.]\
    [Brief Summary: Write a brief summary of the content which includes the respective and relevant product family, tools, or applications. Announce the solution, core message or insight, and take-away of the KBA. Go into detail for the solution by providing information on a granular level, e.g. exact threshold numbers or minimum and maximum values. Do not exceed the length of 160 characters.]\
    [Body: The body of the KBA contains all relevant information based on the user prompt and is structurally organized in several paragraphs with expressive sub-headings. Content-wise, cover the topic comprehensively and provide in-depth technical detail which is relevant for the topic. Style-wise, use headers, bullet points, and lists to organize the text. Make suggestions for relevant images or media files which can enrich a reader’s understanding. Do not exceed the length of 600 words.]\
    [Wrap-up: End with a strong statement which is reassuring, positive and convincing and communicates clearly the key take-away. If a problem can be tested via simulation with Infineon simulation tools, provide this information here.]\
    [Related information: Always provide a list of relevant documents which are related to the exact product or application in question, e.g. datasheets, reference manuals, application notes, code examples, sample projects, user guides, blogs, or KBAs.]\
    \
    If considered useful, add practical examples, troubleshooting tips, or comparisons with alternative solutions or Infineon products."""

        self.summaryprompt = 'You are given a discussion on a case a customer generated, now for closig the case we need to provide a summerized technical solution. go through the discussions and provide me a summarized technical solution in one paragraph in not more than 500 words.\
        Focus on providing a summary in freeform text, provide in this formet \
        Issue summary, Resolution of Issue, Key Points \
        input is a JSON array of objects, where each object represents a comment or message in an email thread. \
        Do not include lines like "Let me know if you have any other question", just focus on technical stuff. \
        Do not include anyones name \
        Here is a breakdown of the properties and values \
        1. `Title`: Subject or Title of Case. \
        2. `Description`: Details of question or multipule questions.\
        3. `Comment Number`: This property contains a unique identifier for each comment. \
        4. `Comment`: This property contains the text content of the comment. \
        5. `Date Created`: This property contains the timestamp when the comment was created, in the format `YYYY-MM-DD HH:MM:SS`. \
        6. `From`: This property contains the name or email address of the person who sent the comment. Here is a sample object from the array:\
        {\
        "Title": "USB Roadmap"\
        "Description": "What is new upcoming USB controler from Infineon." \
        "Comment Number": "1",\
        "Comment": "abcd efg",\
        "Date Created": "2024-03-20 06:26:21",\
        "From": "abc"\
        }'

    def Gpt4ifx_kba(self, json_case):
        print("Gpt4ifx_kba")

        client = openai.OpenAI(     
            api_key=self.BasicToken,     
            base_url=self.Gpt4ifxchatUrl,      
            default_headers=self.headers,     
            http_client = httpx.Client(verify=self.cert_path)   
        ) 

        completion = client.chat.completions.create(     
            model=self.Gpt4ifxmodel,     
            messages=[{"role": "system", "content": self.kbaprompt},     
                      {"role":"user", "content": json_case}],     
            max_tokens=4096,     
            stream=False,     
            temperature=0.5,       
        )   
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

