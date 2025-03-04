import numpy as np

# Generate preferences
def generate_preferences(n=100, m=100):
    """Generate random student and project preferences."""
    students = np.array([np.random.permutation(m) for _ in range(n)])  # Student preferences
    projects = np.array([np.random.permutation(n) for _ in range(m)])  # Project preferences
    return students, projects

#Initial random matching
def initial_matching(n, m):
    """Randomly match students to projects."""
    students, projects = generate_preferences(n, m)
    matches = np.random.permutation(m)[:n]  # Assign random projects to students
    return matches, students, projects

#Calculate student satisfaction
def count_satisfaction(matches, students):
    """Calculate total student dissatisfaction (lower is better)."""
    satisfaction = 0
    for i, project in enumerate(matches):
        satisfaction += np.where(students[i] == project)[0][0]  # Rank of assigned project
    return satisfaction

#Calculate project satisfaction
def count_project_satisfaction(matches, projects):
    """Calculate total project dissatisfaction (lower is better)."""
    satisfaction = 0
    for project, student in enumerate(matches):
        satisfaction += np.where(projects[project] == student)[0][0]  # Rank of assigned student
    return satisfaction

#Swap students only if balance improves
def swap_students_balanced(matches, students, projects):
    """Try swapping two students to balance student & project satisfaction."""
    n = len(matches)
    new_matches = matches.copy()

    i, j = np.random.choice(n, 2, replace=False)  # Select two random students
    new_matches[i], new_matches[j] = new_matches[j], new_matches[i]  # Swap their projects

    # Calculate satisfaction before and after swapping
    old_student_satisfaction = count_satisfaction(matches, students)
    old_project_satisfaction = count_project_satisfaction(matches, projects)

    new_student_satisfaction = count_satisfaction(new_matches, students)
    new_project_satisfaction = count_project_satisfaction(new_matches, projects)

    # Keep swap if it improves balance
    old_diff = abs(old_student_satisfaction - old_project_satisfaction)
    new_diff = abs(new_student_satisfaction - new_project_satisfaction)

    if new_diff < old_diff:  # Swap if the balance improves
        return new_matches
    return matches  # Otherwise, keep the old matching

# Optimize assignments while balancing satisfaction
def local_search_balanced(n, m, max_steps=1000):
    """Improve project assignments while balancing student & project satisfaction."""
    matches, students, projects = initial_matching(n, m)
    current_student_satisfaction = count_satisfaction(matches, students)
    current_project_satisfaction = count_project_satisfaction(matches, projects)

    for _ in range(max_steps):
        new_matches = swap_students_balanced(matches, students, projects)
        new_student_satisfaction = count_satisfaction(new_matches, students)
        new_project_satisfaction = count_project_satisfaction(new_matches, projects)

        # Keep change if balance improves
        old_diff = abs(current_student_satisfaction - current_project_satisfaction)
        new_diff = abs(new_student_satisfaction - new_project_satisfaction)

        if new_diff < old_diff:
            matches = new_matches
            current_student_satisfaction = new_student_satisfaction
            current_project_satisfaction = new_project_satisfaction

    return matches, current_student_satisfaction, current_project_satisfaction

# Run optimization
n = 100  # Number of students
m = 100  # Number of projects

matches, student_satisfaction, project_satisfaction = local_search_balanced(n, m)

# Print results
print("\n🔹 Final Matching Results:")
for student, project in enumerate(matches):
    print(f"Student {student} → Project {project}")

print("\n📊 Final Satisfaction Scores:")
print(f"👨‍🎓 Student Satisfaction Score: {student_satisfaction} (Lower is better)")
print(f"🏢 Project Satisfaction Score: {project_satisfaction} (Lower is better)")
print(f"⚖️ Balance Difference: {abs(student_satisfaction - project_satisfaction)} (Smaller is better)")

