from classes.EntityConverter import EntityConverter
from classes.DatasetGenerator import DatasetGenerator
from tqdm import tqdm
import os

class PSLFileBuilder():
    def __init__(self, train_triples =[], val_triples=[], entity_converter = [] ):
        self.train_triples = train_triples
        self.val_triples = val_triples
        self.entity_converter = entity_converter
        self.generator = DatasetGenerator()

    def build_map_files(self, seperator = "%20"): 
        for relindex,name in tqdm(self.entity_converter.relindex_to_name.items()):        
            f = open(f"data/map/{self.generator.encode_text(name)}_map.txt", "a",  encoding="utf-8")
            first_line = True
            items_added = set()
            for h,r,t in tqdm(self.train_triples):
                if r != relindex or t in items_added:#Avoid adding duplicates to the map
                    continue 
                items_added.add(t)
                t_map_name = self.generator.encode_text(self.entity_converter.entityindex_to_name[t])
                if first_line:
                  f.write(f"{t}\t{t_map_name}")
                  first_line = False
                else:
                  f.write(f"\n{t}\t{t_map_name}")
            f.close()

    def build_obs_files(self):    
        for relindex,name in tqdm(self.entity_converter.relindex_to_name.items()):       
            f = open(f"data/obs/{self.generator.encode_text(name)}_obs.txt", "w")
            #items_added = set()
            for h,r,t in self.train_triples:
                if r == relindex:
                    f.write(f"{ self.generator.encode_text( self.entity_converter.entityindex_to_name[h])}\t{self.generator.encode_text(self.entity_converter.entityindex_to_name[t])}\t1.0\n") 
                
            """        
            for headindex,headname in self.entity_converter.entityindex_to_name.items():  
                for tailindex,tailname in self.entity_converter.entityindex_to_name.items(): 
                    if headindex == tailindex:
                        continue
                    if (headindex, tailindex) in items_added:
                        f.write(f"{headindex}\t{tailindex}\t1.0\n")
                    else:
                        f.write(f"{headindex}\t{tailindex}\t0.0\n")
            """
            f.close()            
    
    def build_target_files(self):
        for relindex,name in tqdm(self.entity_converter.relindex_to_name.items()):       
            f = open(f"data/targets/{self.generator.encode_text(name)}_targets.txt", "w")
            #items_added = set()
            for h,r,t in self.val_triples:
                if r == relindex:
                    f.write(f"{ self.generator.encode_text( self.entity_converter.entityindex_to_name[h])}\t{self.generator.encode_text(self.entity_converter.entityindex_to_name[t])}\n") 
            f.close()    
    
    def build_truth_files(self):
        for relindex,name in tqdm(self.entity_converter.relindex_to_name.items()):       
            f = open(f"data/truth/{self.generator.encode_text(name)}_truth.txt", "w")
            #items_added = set()
            for h,r,t in self.val_triples:
                if r == relindex:
                    f.write(f"{ self.generator.encode_text( self.entity_converter.entityindex_to_name[h])}\t{self.generator.encode_text(self.entity_converter.entityindex_to_name[t])}\t1.0\n") 
            f.close()         

    