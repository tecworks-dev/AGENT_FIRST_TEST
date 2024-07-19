
"""
This module handles fine-tuning and training of AI models.
It provides functionality for preparing training data, fine-tuning models,
and evaluating model performance.
"""

from typing import List, Dict
from app.utils.api_utils import AsyncAnthropic
import os
import asyncio
import logging
import traceback

class AITrainingService:
    def __init__(self):
        self.anthropic = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.logger = logging.getLogger(__name__)

    async def prepare_training_data(self, data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Prepares and formats the training data for model fine-tuning.

        Args:
            data (List[Dict[str, str]]): Raw training data.

        Returns:
            List[Dict[str, str]]: Formatted training data ready for fine-tuning.
        """
        try:
            formatted_data = []
            for item in data:
                if 'input' in item and 'output' in item:
                    formatted_item = {
                        "prompt": item['input'],
                        "completion": item['output']
                    }
                    formatted_data.append(formatted_item)
                else:
                    self.logger.warning(f"Skipping malformed data item: {item}")
            
            if not formatted_data:
                raise ValueError("No valid training data items found")

            return formatted_data
        except Exception as e:
            self.logger.error(f"Error in prepare_training_data: {str(e)}")
            self.logger.debug(traceback.format_exc())
            raise

    async def fine_tune_model(self, model_name: str, training_data: List[Dict[str, str]]) -> str:
        """
        Fine-tunes an AI model using the provided training data.

        Args:
            model_name (str): Name of the model to fine-tune.
            training_data (List[Dict[str, str]]): Prepared training data.

        Returns:
            str: ID of the fine-tuned model.
        """
        try:
            if not training_data:
                raise ValueError("Training data is empty")

            # Note: This is a placeholder for the actual fine-tuning process
            # In a real implementation, you would use the Anthropic API or another
            # service to perform the fine-tuning
            self.logger.info(f"Fine-tuning model {model_name} with {len(training_data)} examples")
            
            # Simulate fine-tuning process
            await asyncio.sleep(5)  # Simulate processing time
            
            fine_tuned_model_id = f"{model_name}_fine_tuned_{len(training_data)}"
            self.logger.info(f"Fine-tuning complete. New model ID: {fine_tuned_model_id}")

            return fine_tuned_model_id
        except Exception as e:
            self.logger.error(f"Error in fine_tune_model: {str(e)}")
            self.logger.debug(traceback.format_exc())
            raise

    async def evaluate_model_performance(self, model_name: str, test_data: List[Dict[str, str]]) -> Dict[str, float]:
        """
        Evaluates the performance of a fine-tuned model using test data.

        Args:
            model_name (str): Name of the model to evaluate.
            test_data (List[Dict[str, str]]): Test data for evaluation.

        Returns:
            Dict[str, float]: Performance metrics (e.g., accuracy, F1 score).
        """
        try:
            if not test_data:
                raise ValueError("Test data is empty")

            self.logger.info(f"Evaluating model {model_name} with {len(test_data)} test examples")

            # Placeholder for actual evaluation logic
            # In a real implementation, you would run the model on test data and compute metrics
            correct_predictions = 0
            total_predictions = len(test_data)

            for item in test_data:
                # Simulate model prediction
                predicted_output = await self.anthropic.messages.create(
                    model=model_name,
                    max_tokens=100,
                    messages=[{"role": "user", "content": item['input']}]
                )
                
                if predicted_output.content[0].text.strip() == item['output'].strip():
                    correct_predictions += 1

            accuracy = correct_predictions / total_predictions
            
            # Calculate F1 score (simplified, assumes binary classification)
            precision = accuracy  # Simplified
            recall = accuracy  # Simplified
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            performance_metrics = {
                "accuracy": accuracy,
                "f1_score": f1_score
            }

            self.logger.info(f"Evaluation complete. Metrics: {performance_metrics}")
            return performance_metrics
        except Exception as e:
            self.logger.error(f"Error in evaluate_model_performance: {str(e)}")
            self.logger.debug(traceback.format_exc())
            raise

if __name__ == "__main__":
    # This block allows for testing the AITrainingService independently
    async def test_ai_training_service():
        service = AITrainingService()
        
        # Test data
        sample_data = [
            {"input": "What is the capital of France?", "output": "Paris"},
            {"input": "Who wrote Romeo and Juliet?", "output": "William Shakespeare"}
        ]
        
        try:
            prepared_data = await service.prepare_training_data(sample_data)
            print("Prepared data:", prepared_data)
            
            fine_tuned_model = await service.fine_tune_model("test_model", prepared_data)
            print("Fine-tuned model ID:", fine_tuned_model)
            
            performance = await service.evaluate_model_performance(fine_tuned_model, sample_data)
            print("Model performance:", performance)
        except Exception as e:
            print(f"Error during testing: {str(e)}")

    asyncio.run(test_ai_training_service())
