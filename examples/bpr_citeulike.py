from openrec import ModelTrainer
from openrec.utils import Dataset
from openrec.recommenders import BPR
from openrec.utils.evaluators import AUC
from openrec.utils.samplers import RandomPairwiseSampler
from openrec.utils.samplers import EvaluationSampler
import dataloader

raw_data = dataloader.load_citeulike()
dim_embed = 50
total_it = int(1e5)
batch_size = 1000
eval_it = 10000
save_it = eval_it

train_dataset = Dataset(raw_data['train_data'], raw_data['max_user'], raw_data['max_item'], name='Train')
val_dataset = Dataset(raw_data['val_data'], raw_data['max_user'], raw_data['max_item'], name='Val', num_negatives=500)
test_dataset = Dataset(raw_data['test_data'], raw_data['max_user'], raw_data['max_item'], name='Test', num_negatives=500)

train_sampler = RandomPairwiseSampler(batch_size=batch_size, dataset=train_dataset, num_process=5)
val_sampler = EvaluationSampler(batch_size=batch_size, dataset=val_dataset)
test_sampler = EvaluationSampler(batch_size=batch_size, dataset=test_dataset)

bpr_model = BPR(batch_size=batch_size, total_users=train_dataset.total_users(), total_items=train_dataset.total_items(), 
                dim_user_embed=dim_embed, dim_item_embed=dim_embed, save_model_dir='bpr_recommender/', train=True, serve=True)

model_trainer = ModelTrainer(model=bpr_model)

auc_evaluator = AUC()
model_trainer.train(total_it=total_it, eval_it=eval_it, save_it=save_it, train_sampler=train_sampler, 
                    eval_samplers=[val_sampler, test_sampler], evaluators=[auc_evaluator])