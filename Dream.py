    def reflect(self):
        """
        Consolidates episodic rooms into high-stability semantic knowledge.
        Reduces fragmentation and strengthens the 'Scent' of the memory.
        """
        if len(self.rooms) < 10: return

        # 1. Identify "Low Stability" clusters (The Brain Pudding)
        pudding_rooms = [r for r in self.rooms if r["meta"]["stability"] < 0.6]
        
        if len(pudding_rooms) > 5:
            # Sort by similarity to find a theme
            # (In a real implementation, we'd use a Centroid/Mean)
            pudding_rooms.sort(key=lambda x: x["meta"]["ts"])
            
            # 2. Extract the 'Essence'
            # Here we simulate the AI summarizing these into one room
            summary_text = f"Consolidated insight from {len(pudding_rooms)} interactions: " + \
                           " / ".join([r["text"][:30] for r in pudding_rooms[:3]]) + "..."
            
            # 3. Create a High-Order Semantic Room
            new_id = self.add(
                text=summary_text,
                kind="semantic",
                metadata={"consolidated": True, "source_count": len(pudding_rooms)}
            )
            
            # 4. Burn the old, low-value rooms to clear the 'pathways'
            pudding_ids = {r["id"] for r in pudding_rooms}
            self.rooms = [r for r in self.rooms if r["id"] not in pudding_ids]
            
            # Clean up graph edges
            for pid in pudding_ids:
                self.graph.pop(pid, None)
                for neighbors in self.graph.values():
                    neighbors.pop(pid, None)
