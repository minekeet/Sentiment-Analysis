from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TextAnalysisForm, PdfAnalysisForm, VoiceAnalysisForm
from .models import AnalysisResult
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import PyPDF2
import io
import speech_recognition as sr
from pydub import AudioSegment
import os
nltk.download('vader_lexicon', quiet=True)
sid = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    scores = sid.polarity_scores(text)
    pos_percent = scores['pos'] * 100
    neg_percent = scores['neg'] * 100
    neu_percent = scores['neu'] * 100
    return pos_percent, neg_percent, neu_percent

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.
    :param pdf_file: Uploaded PDF file object
    :return: Extracted text as a string, or None if an error occurs
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def home(request):
    text_form = TextAnalysisForm()
    pdf_form = PdfAnalysisForm()
    voice_form = VoiceAnalysisForm()
    return render(request, "home.html", {"text_form": text_form, "pdf_form": pdf_form,"voice_form": voice_form})

def analyze_text(request):
    if request.method == "POST":
        form = TextAnalysisForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            pos, neg, neu = analyze_sentiment(text)
            AnalysisResult.objects.create(input_text=text, positive_percent=pos, negative_percent=neg, neutral_percent=neu)
            return render(request, "result.html", {"pos": pos, "neg": neg, "neu": neu})
    else:
        return redirect("home")
def analyze_pdf(request):
    if request.method == "POST":
            form = PdfAnalysisForm(request.POST, request.FILES)
            if form.is_valid():
                pdf_file = request.FILES["pdf_file"]
                
                # Extract text from the PDF
                text = extract_text_from_pdf(pdf_file)
                if not text:
                    return HttpResponse("Error: Unable to extract text from the PDF file.", status=400)
                
                # Analyze sentiment (replace with your actual sentiment analysis logic)
                pos, neg, neu = analyze_sentiment(text)
                
                # Save the analysis result to the database
                AnalysisResult.objects.create(
                    input_text=text,
                    positive_percent=pos,
                    negative_percent=neg,
                    neutral_percent=neu
                )
                
                # Render the result page
                return render(request, "result.html", {"pos": pos, "neg": neg, "neu": neu})
            else:
                # Handle invalid form submission
                return HttpResponse("Invalid form submission. Please check your input.", status=400)
    else:
            # Redirect to the home page if the request method is not POST
            return redirect("home")


def analyze_voice(request):
    if request.method == "POST":
            form = VoiceAnalysisForm(request.POST, request.FILES)
            if form.is_valid():
                audio_file = request.FILES["audio_file"]
                
                try:
                    # Convert audio file to WAV format if it's not already
                    if not audio_file.name.lower().endswith('.wav'):
                        audio = AudioSegment.from_file(audio_file)
                         # Extract file name without extension and add .wav extension
                        file_name = os.path.splitext(audio_file.name)[0]
                        wav_file_path = f'{file_name}.wav'

                        audio.export(wav_file_path, format="wav")
                        audio_file = open(wav_file_path, "rb")
                        
                    r = sr.Recognizer()
                    with sr.AudioFile(audio_file) as source:
                        audio = r.record(source)
                    
                    try:
                         text = r.recognize_google(audio)
                    except sr.UnknownValueError:
                        return HttpResponse("Could not understand audio", status=400)
                    except sr.RequestError as e:
                        return HttpResponse(f"Could not request results from Google Speech Recognition service; {e}", status=500)
                    
                    pos, neg, neu = analyze_sentiment(text)
                    AnalysisResult.objects.create(
                            input_text=text,
                            positive_percent=pos,
                            negative_percent=neg,
                            neutral_percent=neu
                        )
                    if not audio_file.name.lower().endswith('.wav'):
                        os.remove(wav_file_path)
                    
                    return render(request, "result.html", {"pos": pos, "neg": neg, "neu": neu})


                except Exception as e:
                      return HttpResponse(f"Error processing audio file: {e}", status=500)
            else:
                return HttpResponse("Invalid form submission. Please check your audio file.", status=400)
    else:
         return redirect("home")