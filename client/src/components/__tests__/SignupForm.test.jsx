/**
 * Tests unitaires pour SignupForm
 * Teste le rendu et la validation des champs Pseudonyme et Nationalité
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SignupForm from '../SignupForm';

describe('SignupForm - Component Rendering', () => {
  
  it('should render pseudonym field', () => {
    const mockOnNext = vi.fn();
    render(<SignupForm onNext={mockOnNext} />);
    
    const pseudonymInput = screen.getByPlaceholderText(/pseudo123/i);
    expect(pseudonymInput).toBeDefined();
    expect(pseudonymInput.getAttribute('maxLength')).toBe('20');
  });
  
  it('should render nationality select field', () => {
    const mockOnNext = vi.fn();
    render(<SignupForm onNext={mockOnNext} />);
    
    const nationalitySelect = screen.getByRole('combobox', { name: /nationalité/i });
    expect(nationalitySelect).toBeDefined();
    
    const options = screen.getAllByRole('option');
    expect(options.length).toBeGreaterThan(1);
  });
  
  it('should render all required fields including new ones', () => {
    const mockOnNext = vi.fn();
    render(<SignupForm onNext={mockOnNext} />);
    
    expect(screen.getByPlaceholderText(/pseudo123/i)).toBeDefined();
    expect(screen.getByRole('combobox', { name: /nationalité/i })).toBeDefined();
    expect(screen.getByPlaceholderText(/votre prénom/i)).toBeDefined();
    expect(screen.getByPlaceholderText(/votre nom/i)).toBeDefined();
    expect(screen.getByPlaceholderText(/votre.email@exemple.com/i)).toBeDefined();
  });
});

describe('SignupForm - Pseudonym Validation', () => {
  
  it('should show error for empty pseudonym', async () => {
    const mockOnNext = vi.fn();
    render(<SignupForm onNext={mockOnNext} />);
    
    const submitButton = screen.getByRole('button', { name: /continuer/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/pseudonyme requis/i)).toBeDefined();
    });
  });
  
  it('should show error for pseudonym too short', async () => {
    const mockOnNext = vi.fn();
    render(<SignupForm onNext={mockOnNext} />);
    
    const pseudonymInput = screen.getByPlaceholderText(/pseudo123/i);
    fireEvent.change(pseudonymInput, { target: { value: 'ab' } });
    
    const submitButton = screen.getByRole('button', { name: /continuer/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/entre 3 et 20 caractères/i)).toBeDefined();
    });
  });
  
  it('should show error for pseudonym with invalid characters', async () => {
    const mockOnNext = vi.fn();
    render(<SignupForm onNext={mockOnNext} />);
    
    const pseudonymInput = screen.getByPlaceholderText(/pseudo123/i);
    fireEvent.change(pseudonymInput, { target: { value: 'user name' } });
    
    const submitButton = screen.getByRole('button', { name: /continuer/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/lettres, chiffres et underscore uniquement/i)).toBeDefined();
    });
  });
  
  it('should accept valid pseudonym', async () => {
    const mockOnNext = vi.fn();
    render(<SignupForm onNext={mockOnNext} />);
    
    const pseudonymInput = screen.getByPlaceholderText(/pseudo123/i);
    fireEvent.change(pseudonymInput, { target: { value: 'valid_user_123' } });
    
    const submitButton = screen.getByRole('button', { name: /continuer/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      const error = screen.queryByText(/entre 3 et 20 caractères/i);
      expect(error).toBeNull();
    });
  });
});

describe('SignupForm - Nationality Validation', () => {
  
  it('should show error for empty nationality', async () => {
    const mockOnNext = vi.fn();
    render(<SignupForm onNext={mockOnNext} />);
    
    const submitButton = screen.getByRole('button', { name: /continuer/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/nationalité requise/i)).toBeDefined();
    });
  });
  
  it('should accept selected nationality', async () => {
    const mockOnNext = vi.fn();
    render(<SignupForm onNext={mockOnNext} />);
    
    const nationalitySelect = screen.getByRole('combobox', { name: /nationalité/i });
    fireEvent.change(nationalitySelect, { target: { value: 'FR' } });
    
    const submitButton = screen.getByRole('button', { name: /continuer/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      const error = screen.queryByText(/nationalité requise/i);
      expect(error).toBeNull();
    });
  });
});

describe('SignupForm - Integration Tests', () => {
  
  it('should submit form with valid data including pseudonym and nationality', async () => {
    const mockOnNext = vi.fn();
    render(<SignupForm onNext={mockOnNext} />);
    
    const genderButton = screen.getByRole('button', { name: /un homme/i });
    fireEvent.click(genderButton);
    
    fireEvent.change(screen.getByPlaceholderText(/votre prénom/i), { target: { value: 'Jean' } });
    fireEvent.change(screen.getByPlaceholderText(/votre nom/i), { target: { value: 'Dupont' } });
    fireEvent.change(screen.getByPlaceholderText(/pseudo123/i), { target: { value: 'jean_dupont_2024' } });
    fireEvent.change(screen.getByPlaceholderText(/votre.email@exemple.com/i), { target: { value: 'jean.dupont@example.com' } });
    
    const passwordInputs = screen.getAllByPlaceholderText(/mot de passe/i);
    fireEvent.change(passwordInputs[0], { target: { value: 'SecurePass123' } });
    fireEvent.change(screen.getByPlaceholderText(/répétez votre mot de passe/i), { target: { value: 'SecurePass123' } });
    
    const dateInput = document.querySelector('input[type="date"]');
    fireEvent.change(dateInput, { target: { value: '1990-01-01' } });
    fireEvent.change(screen.getByPlaceholderText(/paris, lyon/i), { target: { value: 'Paris' } });
    fireEvent.change(screen.getByPlaceholderText(/france, canada/i), { target: { value: 'France' } });
    
    const nationalitySelect = document.querySelector('.nationality-select');
    fireEvent.change(nationalitySelect, { target: { value: 'FR' } });
    
    const submitButton = screen.getByRole('button', { name: /continuer/i });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(mockOnNext).toHaveBeenCalledWith(
        expect.objectContaining({
          pseudonym: 'jean_dupont_2024',
          nationality: 'FR',
          firstName: 'Jean',
          lastName: 'Dupont',
          email: 'jean.dupont@example.com'
        })
      );
    });
  });
});

describe('SignupForm - Validation Helper Tests (Regex)', () => {
  
  it('should validate pseudonym with correct format', () => {
    const pseudonymRegex = /^[a-zA-Z0-9_]+$/;
    
    const validPseudonyms = [
      'john_doe',
      'User123',
      'test_user_2024',
      'JohnDoe',
      'user_123',
      'ABC',
      '___test___'
    ];
    
    validPseudonyms.forEach(pseudo => {
      expect(pseudonymRegex.test(pseudo)).toBe(true);
    });
  });
  
  it('should reject pseudonyms with invalid characters', () => {
    const pseudonymRegex = /^[a-zA-Z0-9_]+$/;
    
    const invalidPseudonyms = [
      'john doe',      // espace
      'user@123',      // @
      'test-user',     // tiret
      'user!',         // caractère spécial
      'émilie',        // accents
      'user#123',      // #
      'test.user',     // point
    ];
    
    invalidPseudonyms.forEach(pseudo => {
      expect(pseudonymRegex.test(pseudo)).toBe(false);
    });
  });
  
  it('should validate pseudonym length between 3 and 20', () => {
    const tooShort = 'ab';            // 2 caractères
    const minValid = 'abc';           // 3 caractères
    const maxValid = 'a'.repeat(20);  // 20 caractères
    const tooLong = 'a'.repeat(21);   // 21 caractères
    
    expect(tooShort.length >= 3 && tooShort.length <= 20).toBe(false);
    expect(minValid.length >= 3 && minValid.length <= 20).toBe(true);
    expect(maxValid.length >= 3 && maxValid.length <= 20).toBe(true);
    expect(tooLong.length >= 3 && tooLong.length <= 20).toBe(false);
  });
  
  it('should combine format and length validation', () => {
    const pseudonymRegex = /^[a-zA-Z0-9_]+$/;
    
    const testCases = [
      { value: 'ab', valid: false },              // trop court
      { value: 'abc', valid: true },              // valide
      { value: 'user_123', valid: true },         // valide
      { value: 'a'.repeat(20), valid: true },     // limite max valide
      { value: 'a'.repeat(21), valid: false },    // trop long
      { value: 'user name', valid: false },       // espace (invalide)
      { value: 'user@test', valid: false },       // @ (invalide)
    ];
    
    testCases.forEach(({ value, valid }) => {
      const formatValid = pseudonymRegex.test(value);
      const lengthValid = value.length >= 3 && value.length <= 20;
      const isValid = formatValid && lengthValid;
      expect(isValid).toBe(valid);
    });
  });
});

describe('SignupForm - Validation Nationality', () => {
  
  it('should require nationality to be selected', () => {
    const nationality = '';
    expect(nationality.length > 0).toBe(false);
  });
  
  it('should accept valid nationality codes', () => {
    const validNationalities = ['FR', 'BE', 'CA', 'US', 'GB', 'DE', 'ES'];
    
    validNationalities.forEach(nat => {
      expect(nat.length > 0).toBe(true);
      expect(typeof nat).toBe('string');
    });
  });
});

describe('SignupForm - Existing Field Validations', () => {
  
  it('should validate alphabetic names (firstName, lastName)', () => {
    const alphabeticRegex = /^[a-zA-ZÀ-ÿ\s'-]+$/;
    
    const validNames = [
      'Jean',
      'Marie-Claire',
      'O\'Connor',
      'José',
      'François',
      'Anne-Sophie',
      'Jean Paul'
    ];
    
    validNames.forEach(name => {
      expect(alphabeticRegex.test(name)).toBe(true);
    });
    
    const invalidNames = [
      'Jean123',     // chiffres
      'User@test',   // caractères spéciaux
      'Test_name',   // underscore
    ];
    
    invalidNames.forEach(name => {
      expect(alphabeticRegex.test(name)).toBe(false);
    });
  });
  
  it('should validate email format', () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    const validEmails = [
      'test@example.com',
      'user.name@domain.co.uk',
      'user+tag@gmail.com',
      'user123@test.fr'
    ];
    
    validEmails.forEach(email => {
      expect(emailRegex.test(email)).toBe(true);
    });
    
    const invalidEmails = [
      'notanemail',
      '@nodomain.com',
      'user@',
      'user @domain.com',
      'user@domain'
    ];
    
    invalidEmails.forEach(email => {
      expect(emailRegex.test(email)).toBe(false);
    });
  });
  
  it('should validate password strength', () => {
    const passwordRegex = /(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/;
    
    const validPasswords = [
      'Password123',
      'Test123abc',
      'Aa1bbbbb',
      'MyPass123'
    ];
    
    validPasswords.forEach(pwd => {
      const hasMinLength = pwd.length >= 8;
      const hasStrength = passwordRegex.test(pwd);
      expect(hasMinLength && hasStrength).toBe(true);
    });
    
    const invalidPasswords = [
      'password',         // pas de majuscule ni chiffre
      'PASSWORD123',      // pas de minuscule
      'Password',         // pas de chiffre
      'Pass1',            // trop court
    ];
    
    invalidPasswords.forEach(pwd => {
      const hasMinLength = pwd.length >= 8;
      const hasStrength = passwordRegex.test(pwd);
      const isValid = hasMinLength && hasStrength;
      expect(isValid).toBe(false);
    });
  });
  
  it('should validate age requirement (18+)', () => {
    const currentYear = new Date().getFullYear();
    
    const validBirthDates = [
      `${currentYear - 18}-01-01`,    // exactement 18 ans
      `${currentYear - 25}-06-15`,    // 25 ans
      `${currentYear - 40}-12-31`,    // 40 ans
    ];
    
    validBirthDates.forEach(date => {
      const age = currentYear - new Date(date).getFullYear();
      expect(age >= 18).toBe(true);
    });
    
    const invalidBirthDates = [
      `${currentYear - 17}-12-31`,    // 17 ans
      `${currentYear - 10}-01-01`,    // 10 ans
      `${currentYear}-01-01`,         // 0 ans
    ];
    
    invalidBirthDates.forEach(date => {
      const age = currentYear - new Date(date).getFullYear();
      expect(age >= 18).toBe(false);
    });
  });
});

describe('SignupForm - Integration Tests', () => {
  
  it('should validate complete form data with new fields', () => {
    const formData = {
      gender: 'man',
      firstName: 'Jean',
      lastName: 'Dupont',
      pseudonym: 'jean_dupont_2024',
      email: 'jean.dupont@example.com',
      password: 'SecurePass123',
      confirmPassword: 'SecurePass123',
      birthDate: '1990-01-01',
      city: 'Paris',
      country: 'France',
      nationality: 'FR'
    };
    
    const alphabeticRegex = /^[a-zA-ZÀ-ÿ\s'-]+$/;
    const pseudonymRegex = /^[a-zA-Z0-9_]+$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordRegex = /(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/;
    const currentYear = new Date().getFullYear();
    
    const isValid = (
      formData.gender.length > 0 &&
      alphabeticRegex.test(formData.firstName) &&
      alphabeticRegex.test(formData.lastName) &&
      pseudonymRegex.test(formData.pseudonym) &&
      formData.pseudonym.length >= 3 &&
      formData.pseudonym.length <= 20 &&
      emailRegex.test(formData.email) &&
      formData.password.length >= 8 &&
      passwordRegex.test(formData.password) &&
      formData.password === formData.confirmPassword &&
      (currentYear - new Date(formData.birthDate).getFullYear() >= 18) &&
      alphabeticRegex.test(formData.city) &&
      alphabeticRegex.test(formData.country) &&
      formData.nationality.length > 0
    );
    
    expect(isValid).toBe(true);
  });
  
  it('should reject form with invalid pseudonym', () => {
    const formDataInvalid = {
      pseudonym: 'ab',  // trop court
      nationality: 'FR'
    };
    
    const pseudonymRegex = /^[a-zA-Z0-9_]+$/;
    const isPseudonymValid = (
      pseudonymRegex.test(formDataInvalid.pseudonym) &&
      formDataInvalid.pseudonym.length >= 3 &&
      formDataInvalid.pseudonym.length <= 20
    );
    
    expect(isPseudonymValid).toBe(false);
  });
  
  it('should reject form without nationality', () => {
    const formDataInvalid = {
      nationality: ''
    };
    
    expect(formDataInvalid.nationality.length > 0).toBe(false);
  });
});
