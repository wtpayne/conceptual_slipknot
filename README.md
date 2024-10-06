# **Co-Author**  
**Team:** conceptual_slipknot  
**Members:** Sashank, Bill, Soumya and `Mistral AI`  
**Submission for the London Mistral Hackathon**

---

## **Core Idea:**
**Co-Author** is designed to be a creative co-pilot for authors, enhancing the literary crafting process by generating poetry based on images and themes. Think of it as a control-net for transforming visual art into textual creativity!

---

## **Pipeline Overview:**

1. **Image Input:**
   - Feed an image into the system to identify significant objects using **Pixtral**.

2. **Theme Extraction:**
   - Derive a central theme from the analyzed image.

3. **Contextual Significance:**
   - Understand the significance of the extracted objects in relation to the theme, providing context for creativity.

4. **Poem Generation:**
   - Generate an original poem based on the identified significance and context.

5. **Image Handling:**
   - Introduce a new image at any point. 
   - The system allows for image replacement to keep the creative process dynamic.

6. **Iterative Process:**
   - Repeat Steps 2 & 3 as necessary, refining the theme and context.

7. **Critique Mechanism:**
   - A **LLM-based critic** assesses the relevance of any new additions. 
   - If the new image or poem doesn’t align with the context or quality, it can be regenerated.
   - Note: No critic is applied to the first poem generation.

8. **Dynamic Adaptation:**
   - Both the poem and the image can be modified at any point, ensuring relevancy and coherence throughout the creative journey.

---

## ** To Use: **
run `run` :P


## **Technical Notes:**
- To utilize the Mistral API: 
  ```bash
  pip install mistralai 
