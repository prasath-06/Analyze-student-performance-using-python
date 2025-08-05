import json
class Student_Manager:
    def __init__(self):
        self.students={}
    def create_student(self,name,s_id,batch):
        self.students[s_id]={
            "name":name,
            "batch":batch,
            "attendance":{
                "total_days":0,
                "present_days":0
            },
            "terms":{}
        }
    
    def add_term_results(self,s_id,term_name,subjectMarks):
        if s_id in self.students:
            self.students[s_id]["terms"][term_name]=subjectMarks
            
            
    def update_marks(self,s_id,term,subject,new_mark):
        if s_id in self.students:
            self.students[s_id]["terms"][term][subject]= new_mark
        else:
            return "student not found"
    
    def attendance(self,s_id,total,present):
        if s_id in self.students:
            self.students[s_id]["attendance"]["total_days"]+=total
            self.students[s_id]["attendance"]["present_days"]+=present
            
    def calculate_average(self,s_id):
        if s_id not in self.students:
            return 0
        total=0
        count=0
        terms=self.students[s_id]["terms"]
        for i in terms.values():
            for mark in i.values():
                total+=mark
                count+=1
        avg=total/count
        percentage=round(avg,2)
        if percentage>0:
            return percentage
            
    def calculate_attendance(self,s_id):
        att=self.students[s_id]["attendance"]
        if s_id in self.students:
            if att["total_days"]==0:
                return 0.0
            else:
                attendance=round(att["present_days"]/att["total_days"],2)
        return attendance*100
    
    def topper(self,term):
        highest_avg=0
        topper=None
        for s_id,data in self.students.items():
            if term in data["terms"]:
                marks=data["terms"][term].values()
                avg=round(sum(marks)/len(marks),2)
                if avg>highest_avg:
                    highest_avg=avg
                    topper=(data["name"],s_id,highest_avg)
        return topper
        
    def overall_average(self,batch):
        rank=[]
        for s_id,data in self.students.items():
            if data["batch"]==batch:
                avg=self.calculate_average(s_id)
                rank.append((avg,data["name"],s_id))
        rank.sort(reverse=True)
        return rank
        
    def generate_report(self,s_id):
        if s_id in self.students:
            data=self.students[s_id]
            report=f"student report:{data['name']} ({s_id})\n"
            report+=f"Batch: {data['batch']}\n"
            report+=f"attendance:{self.calculate_attendance(s_id)}%\n"
            
            for term,subjects in data["terms"].items():
                avg=sum(subjects.values())/len(subjects)
                avg=round(avg,2)
                report+=f"{term} Average:{avg}\n"
            report+=f"overall average:{self.calculate_average(s_id)}\n"
            return report
    
    def export_data_to_json(self, filename):
        with open(filename, "w") as f:
            json.dump(self.students, f, indent=4)

    def import_data_from_json(self, filename):
        with open(filename, "r") as f:
            self.students = json.load(f)
    
staff=Student_Manager()
staff.create_student("prasath","st01",2025)

staff.add_term_results("st01","Term1",{'tam':90,'eng':90,'mat':90})

staff.create_student("naresh","st02",2025)

staff.add_term_results("st02","Term1",{'tam':90,'eng':90,'mat':90})

staff.update_marks('st02','Term1','mat',80)

staff.attendance("st01",100,70)

staff.calculate_attendance("st01")

staff.calculate_attendance("st02")

staff.calculate_average("st01")

staff.calculate_average("st02")

topper=staff.topper("Term1")
if topper:
    print(f"top performer:{topper[0]} with {topper[2]} average")
print(staff.generate_report("st01"))

print("Top Rankers")
for avg, name, s_id in staff.overall_average(2025):
    print(f"{name} ({s_id}) - {avg}")