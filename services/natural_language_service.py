import os
import streamlit as st
import pandas as pd
import openai
import datetime
from dotenv import load_dotenv
from .code_generator import CodeGenerator
from .visualization import AutoVisualization

load_dotenv()
OPEN_API_KEY = os.getenv("OPEN_AI_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_KEYS = [k.strip() for k in GROK_API_KEY.split(",") if k.strip()]

class NaturalLanguageQuery:  
    def __init__(self):
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        if 'context_memory' not in st.session_state:
            st.session_state.context_memory = {
                'corrections': [],
                'preferences': [],
                'previous_analyses': []
            }

            
    def display_chat_interface(self):
        st.subheader("Ask Questions About the data")        
        if st.session_state.chat_messages is not None:
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    if message["role"] == "assistant" and message.get("type") == "analysis" and message.get("result_data"):
                        result_data = message["result_data"]
                        
                        # expander_title = f"Analysis Results"
                        # if result_data.get("type"):
                            # expander_title += f" ({result_data['type'].title()})"
                        
                        with st.expander("Analysis Results", expanded=True):
                            st.write(message["content"])                            
                            # Show generated code if available
                            if result_data.get("generated_code"):
                                with st.expander("View Generated Code"):
                                    st.code(result_data["generated_code"], language="python")
                            
                            if result_data["type"] == "dataframe":
                                st.dataframe(result_data["content"])
                            elif result_data["type"] == "error":
                                st.error(result_data["content"])
                            elif result_data["type"] in ["number", "text", "unknown"]:
                                st.info(result_data["content"])

                            if result_data.get("visualization"):
                                st.subheader("Visualized Data")
                                st.plotly_chart(result_data["visualization"], use_container_width=True)
                                st.caption("Automatic visualization generated based on given data")

                            # Show narrative if available
                            if result_data.get("narrative"):
                                st.subheader("Summary")
                                st.info(result_data['narrative'])
                    elif message["role"] == "assistant" and message.get("type") == "text_only":
                        # Determine the expander title based on response type
                        response_type = message.get("response_type", "")
                        if response_type == "developer_info":
                            expander_title = "Developer Information"
                        elif response_type == "unrelated_question":
                            expander_title = "Question Not Understood"
                        elif response_type == "chat_history":
                            expander_title = "Chat History & Memory"
                        else:
                            # Fallback to content detection for older messages
                            if "About the Developer" in message["content"]:
                                expander_title = "👨‍💻 Developer Information"
                            elif "I don't understand the question" in message["content"]:
                                expander_title = "Question Not Understood"
                            elif "AI Memory & Chat History" in message["content"]:
                                expander_title = "Chat History & Memory"
                            else:
                                expander_title = "Response"
                        
                        with st.expander(expander_title, expanded=True):
                            st.markdown(message["content"])
                    else:
                        st.write(message["content"])
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Clear History", help="Clear conversation history"):
                st.session_state.chat_messages = []
                st.session_state.conversation_history = []
                st.session_state.context_memory = {
                    'corrections': [],
                    'preferences': [],
                    'previous_analyses': []
                }
                st.rerun()
        
    def get_dataframe_info(self, df):
        columns_info = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            columns_info.append(f"{col} ({dtype})")
        return ", ".join(columns_info)

    def process_user_request(self, user_query, df):
        try:
            # Store the current query in conversation history
            self._add_to_conversation_history(user_query, "user")            
            self._detect_and_store_corrections(user_query)
            
            if self._is_developer_question(user_query):
                return self._handle_developer_question(user_query), None
            
            # Check if user is asking to see chat history
            if self._is_chat_history_request(user_query):
                return self._handle_chat_history_request(), None
            
            if not self._is_data_analysis_question(user_query, df):
                return self._handle_unrelated_question(user_query), None
            
            code_generation = CodeGenerator
            df_info = self.get_dataframe_info(df)
            
            context = self._build_conversation_context()
            
            if context['recent_messages'] or context['corrections'] or context['previous_analyses']:
                st.info("Using conversation history to provide better results")
            
            # with st.spinner("generating analysis code"):
            generated = code_generation.generate_code_with_context(self, user_query, df_info, context)
            # print("generated", generated)
            with st.expander("View Generated Code"):
                st.code(generated, language="python")
            with st.spinner("Executing analysis..."):
                result, error = code_generation.execute_code(self, generated, df)
                # print('code execution,', result, error)
            formatted_result = code_generation.format_executed_code(self, result, error, user_query, df)
            
            # Store the result in conversation history
            self._add_to_conversation_history(formatted_result.get("display", "Analysis completed"), "assistant")
            self._store_analysis_result(user_query, formatted_result, generated)
            
            # print('formatttttt.........', formatted_result)
            return formatted_result, generated
        except Exception as e:
            print("error occur", e)

    def get_user_query(self):
        user_query = st.chat_input("Ask a question about the data...")        
        if user_query:
            st.session_state.chat_messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.write(user_query)            
            return user_query
        return None
    
    def add_assistant_response(self, response, result_data, generated_code=None):
        if result_data and result_data["type"] in ["developer_info", "unrelated_question", "chat_history"]:
            st.session_state.chat_messages.append({
                "role": "assistant", 
                "content": result_data["content"],
                "type": "text_only",
                "response_type": result_data["type"]  # Store the specific response type
            })
        else:
            if generated_code and result_data:
                result_data["generated_code"] = generated_code
            
            st.session_state.chat_messages.append({
                "role": "assistant", 
                "content": response,
                "result_data": result_data,
                "type": "analysis"
            })
            
        with st.chat_message("assistant"):
            if result_data:
                if result_data["type"] == "developer_info":
                    with st.expander("👨‍💻 Developer Information", expanded=True):
                        st.markdown(result_data["content"])
                elif result_data["type"] == "unrelated_question":
                    with st.expander("Question Not Understood", expanded=True):
                        st.markdown(result_data["content"])
                elif result_data["type"] == "chat_history":
                    with st.expander("Chat History & Memory", expanded=True):
                        st.markdown(result_data["content"])
                else:
                    
                    # expander_title = f"Analysis Results"
                    # if result_data.get("type"):
                        # expander_title += f" ({result_data['type'].title()})"
                    
                    with st.expander("Analysis Results", expanded=True):
                        st.write(result_data["display"])                
                        if result_data["type"] == "dataframe":
                            st.dataframe(result_data["content"])
                        elif result_data["type"] == "error":
                            st.error(result_data["content"])
                        elif result_data["type"] in ["number", "text", "unknown"]:
                            st.info(result_data["content"])

                        # if there is a visualization,  show
                        if result_data.get("visualization"):
                            st.subheader("Visualized Data")
                            st.plotly_chart(result_data["visualization"], use_container_width=True)
                            st.caption("Automatic visualization generated based on given data")

                        # if there is a naration show that naration
                        if result_data.get("narrative"):
                            st.subheader("Summary")
                            st.info(result_data['narrative'])
    
    
    def _add_to_conversation_history(self, message, role):
        """Add message to conversation history with timestamp"""
        import datetime
        st.session_state.conversation_history.append({
            "role": role,
            "content": message,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        # Keep only 20 messages, sience am using memory as adb
        if len(st.session_state.conversation_history) > 20:
            st.session_state.conversation_history = st.session_state.conversation_history[-20:]
    
    def _detect_and_store_corrections(self, user_query):
        """Detect if user is providing corrections or feedback"""
        correction_keywords = [
            "wrong", "incorrect", "not right", "that's not", "actually", 
            "correction", "fix", "mistake", "error", "should be", 
            "instead", "rather", "no that's", "not what i meant"
        ]
        
        query_lower = user_query.lower()
        if any(keyword in query_lower for keyword in correction_keywords):
            st.session_state.context_memory['corrections'].append({
                "correction": user_query,
                "timestamp": datetime.datetime.now().isoformat(),
                "previous_context": st.session_state.conversation_history[-3:] if len(st.session_state.conversation_history) >= 3 else st.session_state.conversation_history
            })
    
    def _build_conversation_context(self):
        context = {
            "recent_messages": st.session_state.conversation_history[-6:] if st.session_state.conversation_history else [],
            "corrections": st.session_state.context_memory['corrections'][-3:] if st.session_state.context_memory['corrections'] else [],
            "previous_analyses": st.session_state.context_memory['previous_analyses'][-3:] if st.session_state.context_memory['previous_analyses'] else []
        }
        return context
    
    def _store_analysis_result(self, query, result, code):
        st.session_state.context_memory['previous_analyses'].append({
            "query": query,
            "result_type": result.get("type"),
            "code": code,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        if len(st.session_state.context_memory['previous_analyses']) > 10:
            st.session_state.context_memory['previous_analyses'] = st.session_state.context_memory['previous_analyses'][-10:]
    

    
    def _is_developer_question(self, user_query):
        developer_keywords = [
            "developer", "who made", "who created", "who built", "creator", "Who develop you",
            "who is the developer","who make you?","developer",
            "author", "programmer", "engineer", "contact", "email", 
            "website", "portfolio", "about you", "who are you", "your creator",
            "made this", "built this", "developed this", "ermiyas","who build you?",
            "who build this?","Who are you?","who create this?","who is the developer?",
            "who is the creator?","creator","maker","build","software","engineer","who make this?",
           "who are you?"
        ]
        
        query_lower = user_query.lower()
        return any(keyword in query_lower for keyword in developer_keywords)
    
    def _handle_developer_question(self, user_query):
        developer_info = {
            "name": "Ermiyas Developer",
            "website": "https://ermiyas.dev",
            "email": "inbox@ermiyas.dev",
            "about": "A software engineer that develops many systems."
        }
        
        response_text = f"""
        **About the Developer**
        
        This SparkLite AI system was created by **{developer_info['name']}**, a skilled software engineer who specializes in developing various systems and applications.
        
        **Contact**: {developer_info['email']}
        **Website**: {developer_info['website']}
        
        For more information about the developer's work, projects, and expertise, please visit: **{developer_info['website']}**
        
        If you have questions about data analysis, feel free to ask about your uploaded data!
        """
        self._add_to_conversation_history(response_text, "assistant")
        
        return {
            "type": "developer_info",
            "content": response_text,
            "display": response_text,
            "visualization": None,
            "narrative": None
        }
    
    def _is_data_analysis_question(self, user_query, df):
        query_lower = user_query.lower()
        
        data_keywords = [
            "show", "display", "analyze", "analysis", "calculate", "count", "sum", "average", "mean",
            "total", "maximum", "minimum", "filter", "group", "sort", "chart", "graph", "plot",
            "visualize", "trend", "pattern", "correlation", "distribution", "statistics", "stats",
            "data", "dataset", "table", "column", "row", "value", "sales", "revenue", "profit",
            "customer", "product", "region", "category", "date", "time", "period", "month", "year",
        ]
        
        column_keywords = []
        if df is not None:
            column_keywords = [col.lower() for col in df.columns]
        
        has_data_keywords = any(keyword in query_lower for keyword in data_keywords)
        has_column_keywords = any(keyword in query_lower for keyword in column_keywords)
        
        unrelated_keywords = [
            "weather", "news", "politics", "sports", "entertainment", "music", "movie", "book",
            "recipe", "cooking", "travel", "hotel", "flight", "restaurant", "shopping", "fashion",
            "health", "medicine", "doctor", "hospital", "school", "education", "university",
            "job", "career", "salary", "interview", "resume", "dating", "relationship", "love",
            "game", "gaming", "video game", "social media", "facebook", "twitter", "instagram",
            "cryptocurrency", "bitcoin", "stock market", "investment", "real estate", "car", "vehicle",
            "technology news", "smartphone", "computer hardware", "software review", "app recommendation"
        ]
        
        has_unrelated_keywords = any(keyword in query_lower for keyword in unrelated_keywords)
        
        simple_questions = [
            "hello", "hi", "how are you", "what's up", "good morning", "good afternoon", "good evening",
            "thank you", "thanks", "bye", "goodbye", "see you", "what can you do", "help me",
            "what is", "tell me about", "explain", "define","yoo","what","meaning?","no","yes","ofcourse",
            "who","by","ai"
        ]
        
        is_simple_question = any(question in query_lower for question in simple_questions)
        
        if has_unrelated_keywords:
            return False
        
        if is_simple_question and not (has_data_keywords or has_column_keywords):
            return False
        
        if has_data_keywords or has_column_keywords:
            return True
        
        return True
    
    def _handle_unrelated_question(self, user_query):
        response_text = """
        **I don't understand the question**
        
        I'm SparkLite AI, designed specifically to analyze sales data and generate reports. I can help you with:
        
        **Data Analysis Tasks:**
        - Show sales trends and patterns
        - Calculate totals, averages, and statistics
        - Filter and group data by different criteria
        - Create visualizations and charts
        - Generate summaries and insights
        
        **Example Questions:**
        - "Show me total sales by region"
        - "What's the average revenue per customer?"
        - "Display sales trends over time"
        - "Which products are performing best?"
        
        Please ask a question related to your uploaded data, and I'll be happy to help with the analysis!
        """
        
        self._add_to_conversation_history(response_text, "assistant")
        
        return {
            "type": "unrelated_question",
            "content": response_text,
            "display": response_text,
            "visualization": None,
            "narrative": None
        }
    
    def _is_chat_history_request(self, user_query):
        """Detect if user is asking to see chat history"""
        history_keywords = [
            "show history", "chat history", "conversation history", "show chat", "view history",
            "what did we talk about", "previous conversation", "show memory", "what do you remember",
            "our conversation", "chat log", "message history", "show messages", "previous messages"
        ]
        
        query_lower = user_query.lower()
        return any(keyword in query_lower for keyword in history_keywords)
    
    def _handle_chat_history_request(self):
        """Handle requests to view chat history"""
        # Build the chat history content
        history_content = "**AI Memory & Chat History**\n\n"
        
        # Recent conversation history
        if st.session_state.conversation_history:
            history_content += "###  Recent Conversation (Last 10 messages)\n"
            recent_messages = st.session_state.conversation_history[-10:]
            for i, msg in enumerate(recent_messages, 1):
                role_icon = "👤" if msg["role"] == "user" else "🤖"
                timestamp = msg.get("timestamp", "")
                if timestamp:
                    try:
                        dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        time_str = dt.strftime("%H:%M")
                    except:
                        time_str = ""
                else:
                    time_str = ""
                
                content_preview = msg['content'][:150] + ("..." if len(msg['content']) > 150 else "")
                history_content += f"{role_icon} **Message {i}** {time_str}\n"
                history_content += f"   {content_preview}\n\n"
        
        # Corrections remembered
        if st.session_state.context_memory['corrections']:
            history_content += "### Corrections Remembered\n"
            for i, correction in enumerate(st.session_state.context_memory['corrections'][-5:], 1):
                correction_preview = correction['correction'][:100] + ("..." if len(correction['correction']) > 100 else "")
                history_content += f"{i}. {correction_preview}\n"
            history_content += "\n"
        
        # Previous analyses
        if st.session_state.context_memory['previous_analyses']:
            history_content += "###Previous Analyses\n"
            for i, analysis in enumerate(st.session_state.context_memory['previous_analyses'][-5:], 1):
                query_preview = analysis['query'][:80] + ("..." if len(analysis['query']) > 80 else "")
                history_content += f"{i}. **{analysis['result_type']}**: {query_preview}\n"
            history_content += "\n"
        
        # Summary stats
        history_content += "### Memory Statistics\n"
        history_content += f"- **Total Messages**: {len(st.session_state.conversation_history)}\n"
        history_content += f"- **Corrections Made**: {len(st.session_state.context_memory['corrections'])}\n"
        history_content += f"- **Analyses Performed**: {len(st.session_state.context_memory['previous_analyses'])}\n\n"
        
        history_content += "*This information helps me provide better, context-aware responses based on our conversation!*"
        
        self._add_to_conversation_history(history_content, "assistant")
        
        return {
            "type": "chat_history",
            "content": history_content,
            "display": history_content,
            "visualization": None,
            "narrative": None
        }