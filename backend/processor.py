import networkx as nx
import re

def analyze_dependencies(topics):
    """
    Detects prerequisite relationships between topics using lightweight Jaccard Similarity.
    """
    G = nx.DiGraph()
    for topic in topics:
        G.add_node(topic)
    
    # Pre-tokenize topics for similarity
    def get_tokens(text):
        return set(re.findall(r'\w+', text.lower()))

    topic_tokens = [get_tokens(t) for t in topics]

    if len(topics) > 1:
        for i in range(len(topics)):
            for j in range(i + 1, len(topics)):
                # Jaccard Similarity: Intersection / Union
                set_i = topic_tokens[i]
                set_j = topic_tokens[j]
                
                if not set_i or not set_j: continue
                
                intersection = len(set_i.intersection(set_j))
                union = len(set_i.union(set_j))
                similarity = intersection / union
                
                # If topics are similar, assume earlier one is prerequisite
                if similarity > 0.2:
                    G.add_edge(topics[i], topics[j])

    # Unit-based dependency
    current_unit = None
    for topic in topics:
        if re.match(r'^(UNIT|MODULE|CHAPTER)\s+[IVX\d]+', topic, re.IGNORECASE):
            current_unit = topic
        elif current_unit:
            G.add_edge(current_unit, topic)

    # Ensure it's a DAG (remove cycles if any)
    # Simple cycle removal: if (a,b) and (b,a), keep (a,b) if index of a < index of b
    # But usually syllabus is already somewhat ordered.
    if not nx.is_directed_acyclic_graph(G):
        cycles = list(nx.simple_cycles(G))
        for cycle in cycles:
            # For each cycle, remove the back-edge (where target index < source index)
            # This is a bit naive but works for syllabus flow
            pass
            
    return G

def get_study_order(G):
    try:
        # If there are cycles, we can't do topological sort
        # We'll use a modified approach or just return the syllabus order if it fails
        return list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        # If it contains cycles, fallback to original order
        return list(G.nodes())

# Teacher's Insights & Resources Mapping
MENTOR_TIPS = {
    "introduction": "Don't just memorize definitions. Try to understand the 'Why' behind this field.",
    "basic": "Strong foundations make complex topics easier. Spend extra time here if you're a beginner.",
    "neural": "Think of this as biological inspiration. Visualize the layers and connections.",
    "search": "Algorithms are like recipes. Trace them on paper before coding.",
    "algorithm": "Practice with small examples first. Complexity matters more than syntax.",
    "math": "Focus on the logic, not just the formulas. Use online calculators to verify.",
    "code": "Don't just copy. Type every line and see it fail, then fix it.",
    "hard": "Break this into 3 smaller chunks. Don't try to finish it in one sitting.",
    "exam": "Focus on the core concepts. Past papers are your best friend here."
}

def get_mentor_advice(topic):
    topic_lower = topic.lower()
    for key, tip in MENTOR_TIPS.items():
        if key in topic_lower:
            return tip
    return "Study this topic with a focus on its real-world applications."

def get_resource_links(topic):
    # Generates helpful search links for the student
    query = topic.replace(' ', '+')
    return [
        {"name": "YouTube Tutorial", "url": f"https://www.youtube.com/results?search_query={query}+tutorial"},
        {"name": "GeeksforGeeks", "url": f"https://www.google.com/search?q={query}+geeksforgeeks"},
        {"name": "University Notes", "url": f"https://www.google.com/search?q={query}+lecture+notes+pdf"},
        {"name": "Interview Prep", "url": f"https://www.google.com/search?q={query}+interview+questions+answers"},
        {"name": "Documentation/Wiki", "url": f"https://en.wikipedia.org/wiki/{query}"}
    ]

def classify_topics_fully(ordered_topics):
    easy_keywords = ['introduction', 'basics', 'overview', 'concept', 'history', 'units']
    hard_keywords = ['advanced', 'neural', 'optimization', 'complex', 'inference', 'backpropagation', 'bayesian', 'deep', 'logic']
    
    topic_details = {}
    for topic in ordered_topics:
        score = 2 # Default Medium
        t_lower = topic.lower()
        
        if any(kw in t_lower for kw in easy_keywords):
            score = 1
        elif any(kw in t_lower for kw in hard_keywords):
            score = 3
        
        topic_details[topic] = {
            "difficulty": score,
            "advice": get_mentor_advice(topic),
            "resources": get_resource_links(topic)
        }
    return topic_details

def generate_schedule(ordered_topics, topic_details, total_weeks, hours_per_week, student_level="Beginner"):
    """
    Adaptive Scheduling:
    - Beginner: Spends 50% more time on foundations (Difficulty 1).
    - Advanced: Spends 30% less time on basics and jumps to Hard topics faster.
    """
    # Adjust weights based on student level
    if student_level == "Beginner":
        weights = {1: 2.5, 2: 3, 3: 4} # Extra time for foundations
    elif student_level == "Advanced":
        weights = {1: 0.5, 2: 1.5, 3: 3} # Skip basics, focus on hard
    else: # Intermediate
        weights = {1: 1, 2: 2, 3: 3}
    
    topic_weights = [(t, weights[topic_details[t]["difficulty"]]) for t in ordered_topics]
    total_weight = sum(w for _, w in topic_weights)
    
    if total_weight == 0: total_weight = 1
    
    weight_per_week = total_weight / total_weeks
    
    schedule = []
    current_week_topics = []
    current_week_weight = 0
    week_num = 1
    
    for topic, weight in topic_weights:
        current_week_topics.append(topic)
        current_week_weight += weight
        
        # Determine if we should close the week
        if current_week_weight >= weight_per_week and week_num < total_weeks:
            schedule.append({
                "week": week_num,
                "topics": current_week_topics
            })
            current_week_topics = []
            current_week_weight = 0
            week_num += 1
            
    # Add remaining topics to last week
    if current_week_topics:
        if week_num > total_weeks:
            # Distribute leftover to previous weeks if too many, 
            # or just add to last week
            schedule[-1]["topics"].extend(current_week_topics)
        else:
            schedule.append({
                "week": week_num,
                "topics": current_week_topics
            })
            
    return schedule

# Topic Knowledge Base for Chat
TOPIC_KNOWLEDGE = {
    "introduction": "Artificial Intelligence is about creating systems that can perform tasks that normally require human intelligence, like sensing, reasoning, and learning.",
    "search": "Search algorithms like A* or BFS are used to find the best path from a start to a goal. BFS is blind, while A* uses heuristics to 'see' the most promising direction.",
    "neural": "Neural Networks are inspired by the brain. They consist of layers of nodes that learn to recognize patterns by adjusting connection weights during training.",
    "bayesian": "Bayesian networks use probability to represent uncertain knowledge. It's like a map of how one event makes another event more or less likely.",
    "logic": "Propositional and First-Order Logic are formal languages for representing facts and rules so that the computer can deduce new information from them.",
    "machine learning": "Machine Learning is a subset of AI where computers learn from data rather than being explicitly programmed for every scenario.",
    "supervised": "In supervised learning, the model is trained on labeled data, meaning the computer is given the 'answers' and learns to map inputs to those answers.",
    "heuristic": "A heuristic is a 'rule of thumb' or a shortcut. In A* search, it's an estimate of the distance to the goal, helping the algorithm prioritize the best directions.",
    "backpropagation": "Backpropagation is the 'learning' engine of neural networks. It calculates errors and sends them backward through the network to adjust the weights and improve accuracy.",
    "decision tree": "A Decision Tree is like a flow chart for making decisions based on data. It splits information into branches until it reaches a conclusion.",
    "hard": "This is a complex topic that involves deep technical math or abstract concepts. I suggest looking at the YouTube tutorial in your resource list for a visual explanation.",
}

def chat_with_mentor(topic, user_message):
    message_lower = user_message.lower()
    topic_lower = topic.lower()
    
    # Intent detection
    if any(word in message_lower for word in ["hello", "hi", "hey"]):
        return f"Hi there! I'm ready to help you master {topic}. What's on your mind?"
    
    if any(word in message_lower for word in ["what is", "define", "explain", "understand"]):
        # Try to find specific knowledge
        for key, info in TOPIC_KNOWLEDGE.items():
            if key in topic_lower or key in message_lower:
                return f"Sure! {info} In the context of {topic}, it's a foundational concept you'll need for your exams."
        return f"To understand {topic}, think of it as a way to solve problems using intelligence. It's often broken down into smaller, simpler steps."
        
    if "example" in message_lower:
        return f"A great example of {topic} is how a GPS finds the fastest route or how Netflix recommends movies to you based on what you've watched before."

    if any(word in message_lower for word in ["hard", "difficult", "confused", "stuck"]):
        return f"Don't worry, {topic} is considered one of the tougher parts. I recommend focusing on the basic diagrams first. Have you checked the GeeksforGeeks link I provided?"

    # Fallback
    return f"That's a sharp observation about {topic}. To master this, I suggest you try a practice problem or explain it to a friend. The resource links in your dashboard have some great deep-dives for this!"
